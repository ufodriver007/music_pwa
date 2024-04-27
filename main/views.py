from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from main.permissions import IsOwnerOrReadOnly, UserPermission, SongPermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.contrib.auth.models import User
from main.models import SocialProfile, Playlist, Song
from main.serializers import UserSerializer, PlaylistSerializer, SongSerializer, SocialProfileSerializer
from main.utils import search_song
import requests
from django.core.cache import cache
import os
import json
import logging


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    def perform_create(self, serializer):
        usr = User.objects.create_user(username=serializer.validated_data['username'],
                                       password=serializer.validated_data['password'])
        usr.save()


class PlaylistViewSet(ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend]  # указываем бэкенд фильтрации
    filterset_fields = ['user']  # поля для фильтрации

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id  # Устанавливаем текущего пользователя в поле "user"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class SongViewSet(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [SongPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SearchView(APIView):
    def get(self, request, q):
        # Проверяем есть ли в кэше такой запрос
        cache_data = cache.get(q)
        if cache_data:
            return Response(cache_data)
        else:
            result = search_song(q)
            cache.set(q, result, 86400)  # кэшируем на сутки
            return Response(result)


class VKAuth(APIView):
    def get(self, request):
        logging.basicConfig(level='DEBUG')
        logger = logging.getLogger("my_views")
        try:
            payload = json.loads(request.GET.get('payload'))
            service_token = os.getenv('VK_SERVICE_TOKEN')
            uuid = payload['uuid']
            silent_token = payload['token']

            data = {
                'v': '5.199',
                'token': silent_token,
                'access_token': service_token,
                'uuid': uuid,
            }

            response = requests.post('https://api.vk.com/method/auth.exchangeSilentAuthToken', data=data)
            resp = json.loads(response.text)
            access_token = resp['response']['access_token']
            email = resp['response']['email']
            user_id = resp['response']['user_id']

            if SocialProfile.objects.filter(social_id=user_id).exists():
                logger.debug(f'User with social_id({user_id}) already exists')
                social_prof = SocialProfile.objects.get(social_id=user_id)
                user = User.objects.get(id=social_prof.user.id)
                password = user.first_name + str(user_id) + os.getenv('SITE_SALT')
            else:
                # если пользователь НЕ существует, получаем имя, фамилию
                logger.debug(f'User with social_id({user_id}) does not exist')

                def get_profile_info(token: str):
                    request_data = {
                        "access_token": token,
                        "v": "5.199"
                    }
                    profile_info = requests.post("https://api.vk.com/method/account.getProfileInfo", data=request_data)
                    r = json.loads(profile_info.text)
                    first_name = r['response']['first_name']
                    last_name = r['response']['last_name']
                    return {'first_name': first_name, 'last_name': last_name}

                info = get_profile_info(access_token)
                first_name = info['first_name']
                last_name = info['last_name']

                # создаём экземпляр модели пользователя, заполняем его, сохраняем
                new_user = User.objects.create_user(username=first_name + str(user_id),
                                                    email=email,
                                                    password=first_name + str(user_id) + os.getenv('SITE_SALT'),
                                                    first_name=first_name,
                                                    last_name=last_name)
                new_user.save()
                profile = SocialProfile.objects.create(user=new_user,
                                                       token=access_token,
                                                       social_id=user_id)
                profile.save()
                password = first_name + str(user_id) + os.getenv('SITE_SALT')
                user = new_user

        except Exception as e:
            logger.debug(e)
            user = None
            password = None

        request.session['username'] = user.username
        request.session['password'] = password

        return redirect('index')


class ConnectSongAndPlaylistView(APIView):
    def post(self, request, song_id, playlist_id):
        try:
            song = Song.objects.get(id=song_id)
            playlist = Playlist.objects.get(id=playlist_id)
            playlist.songs.add(song)
            return Response({"ok": "Song added to playlist"})
        except Exception as e:
            return Response({"Error": f"{e}"})


class RemoveConnectSongAndPlayView(APIView):
    def post(self, request, song_id, playlist_id):
        try:
            song = Song.objects.get(id=song_id)
            playlist = Playlist.objects.get(id=playlist_id)
            playlist.songs.remove(song)
            return Response({"ok": "Song removed from playlist"})
        except Exception as e:
            return Response({"Error": f"{e}"})


class IndexView(View):
    def get(self, request):
        username = request.session.get('username')
        password = request.session.get('password')
        if username and password:
            return render(request, 'index.html', {'username': username, 'password': password})
        return render(request, 'index.html')


class SongDownloadingProxy(APIView):
    def get(self, *args, **kwargs):
        url = self.request.GET.get('url')

        if url:
            response = requests.get(url)

            if response.status_code == 200:
                file_content = response.content
                filename = url.split('/')[-1]  # Получаем имя файла из URL
                response = HttpResponse(file_content, content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
            else:
                return HttpResponse('File not found', status=404)
        else:
            return HttpResponse('URL parameter is missing', status=400)

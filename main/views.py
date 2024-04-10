from django.http import HttpResponse
from django.shortcuts import render
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
from main.models import Profile, Playlist, Song
from main.serializers import UserSerializer, PlaylistSerializer, SongSerializer
from main.utils import search_song
import requests
from celery.result import AsyncResult


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    def perform_create(self, serializer):
        print(serializer.validated_data['username'])
        print(serializer.validated_data['password'])
        usr = User.objects.create_user(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        usr.save()


class PlaylistViewSet(ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend]            # указываем бэкенд фильтрации
    filterset_fields = ['user']                        # поля для фильтрации

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id         # Устанавливаем текущего пользователя в поле "user"
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
        # TO DO: Сделать реализацию получения результатов таски
        return Response(search_song(q))


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
        return render(request, 'index.html')


class SongDownloadingProxy(APIView):
    def get(self, song_id):
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

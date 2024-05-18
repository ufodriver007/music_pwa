import os
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from rest_framework import status
from django.contrib.auth.models import User


class AuthenticateTest(TestCase):
    """Login/logout tests"""
    token = None

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='12345qwE')

    def test_login(self):
        data = {
            'username': 'test_user',
            'password': '12345qwE'
        }
        response = self.client.post('/auth/token/login/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('auth_token' in response.data)

    def logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + AuthenticateTest.token)
        response = self.client.post('/auth/token/logout/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SongTest(TestCase):
    token = None

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='12345qwE')
        data = {
            'username': 'test_user',
            'password': '12345qwE'
        }
        response = self.client.post('/auth/token/login/', data, format='json')
        SongTest.token = response.data['auth_token']

    def test_create_song(self):
        data = {
            'name': 'Ausländer',
            'author': 'Rammstein',
            'duration': '230',
            'duration_text': '03:50',
            'url': 'https://cs10-1v4.vkuseraudio.net/QxWUkrEB0IC-d0-seuuGxA1YSwXOXr5dSgcJtL3w.mp3',
        }
        response = self.client.post('/api/v1/song/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_song(self):
        data = {
            'name': 'Ausländer',
            'author': 'Rammstein',
            'duration': '230',
            'duration_text': '03:50',
            'url': 'https://cs10-1v4.vkuseraudio.net/QxWUkrEB0IC-d0-seuuGxA1YSwXOXr5dSgcJtL3w.mp3',
        }
        response = self.client.post('/api/v1/song/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        song_id = response.data['id']

        response = self.client.get(f'/api/v1/song/{song_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_song(self):
        data = {
            'name': 'Ausländer',
            'author': 'Rammstein',
            'duration': '230',
            'duration_text': '03:50',
            'url': 'https://cs10-1v4.vkuseraudio.net/QxWUkrEB0IC-d0-seuuGxA1YSwXOXr5dSgcJtL3w.mp3',
        }
        response = self.client.post('/api/v1/song/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        song_id = response.data['id']

        data = {
            'id': f'{song_id}',
            'name': 'new_song_name',
            'author': 'Rammstein',
            'duration': '230',
            'duration_text': '03:50',
            'url': 'https://example.com/example.mp3',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + SongTest.token, HTTP_ACCEPT="application/json", HTTP_CONTENT_TYPE="application/json;charset=utf-8")
        response = self.client.put(f'/api/v1/song/{song_id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_song(self):
        data = {
            'name': 'Ausländer',
            'author': 'Rammstein',
            'duration': '230',
            'duration_text': '03:50',
            'url': 'https://cs10-1v4.vkuseraudio.net/QxWUkrEB0IC-d0-seuuGxA1YSwXOXr5dSgcJtL3w.mp3',
        }
        response = self.client.post('/api/v1/song/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        song_id = response.data['id']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + SongTest.token)
        response = self.client.delete(f'/api/v1/song/{song_id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PlaylistTest(TestCase):
    token = None
    user_id = None

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='12345qwE')
        data = {
            'username': 'test_user',
            'password': '12345qwE'
        }
        response = self.client.post('/auth/token/login/', data, format='json')
        PlaylistTest.token = response.data['auth_token']

        self.client.credentials(HTTP_ACCEPT="application/json", HTTP_AUTHORIZATION=f'Token {PlaylistTest.token}')
        response = self.client.get('/api/v1/auth/users/me/')
        PlaylistTest.user_id = response.data['id']

    def test_create_playlist(self):
        data = {
            'name': 'New_Playlist'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + PlaylistTest.token)
        response = self.client.post('/api/v1/playlist/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_playlist(self):
        data = {
            'name': 'New_Playlist'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + PlaylistTest.token)
        response = self.client.post('/api/v1/playlist/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        playlist_id = response.data['id']

        response = self.client.get(f'/api/v1/playlist/{playlist_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_playlist(self):
        data = {
            'name': 'New_Playlist'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + PlaylistTest.token)
        response = self.client.post('/api/v1/playlist/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        playlist_id = response.data['id']

        data = {
            'id': playlist_id,
            'name': 'New_Playlist',
            'user': f'{PlaylistTest.user_id}'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + PlaylistTest.token, HTTP_ACCEPT="application/json",
                                HTTP_CONTENT_TYPE="application/json;charset=utf-8")
        response = self.client.put(f'/api/v1/playlist/{playlist_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_playlist(self):
        data = {
            'name': 'New_Playlist'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + PlaylistTest.token)
        response = self.client.post('/api/v1/playlist/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        playlist_id = response.data['id']

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + PlaylistTest.token, HTTP_ACCEPT="application/json",
                                HTTP_CONTENT_TYPE="application/json;charset=utf-8")
        response = self.client.delete(f'/api/v1/playlist/{playlist_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AddSongToPlaylistTest(TestCase):
    token = None

    def test_add_song(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='12345qwE')
        data = {
            'username': 'test_user',
            'password': '12345qwE'
        }
        response = self.client.post('/auth/token/login/', data, format='json')
        AddSongToPlaylistTest.token = response.data['auth_token']

        # create song
        data = {
            'name': 'Ausländer',
            'author': 'Rammstein',
            'duration': '230',
            'duration_text': '03:50',
            'url': 'https://cs10-1v4.vkuseraudio.net/QxWUkrEB0IC-d0-seuuGxA1YSwXOXr5dSgcJtL3w.mp3',
        }
        response = self.client.post('/api/v1/song/', data, format='json')
        song_id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create playlist
        data = {
            'name': 'New_Playlist'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + AddSongToPlaylistTest.token)
        response = self.client.post('/api/v1/playlist/', data, format='json')
        playlist_id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Connecting
        response = self.client.post(f'/api/v1/song/{song_id}/add/{playlist_id}/')
        self.assertTrue('ok' in response.data)

    def test_remove_song(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='12345qwE')
        data = {
            'username': 'test_user',
            'password': '12345qwE'
        }
        response = self.client.post('/auth/token/login/', data, format='json')
        AddSongToPlaylistTest.token = response.data['auth_token']

        # create song
        data = {
            'name': 'Ausländer',
            'author': 'Rammstein',
            'duration': '230',
            'duration_text': '03:50',
            'url': 'https://cs10-1v4.vkuseraudio.net/QxWUkrEB0IC-d0-seuuGxA1YSwXOXr5dSgcJtL3w.mp3',
        }
        response = self.client.post('/api/v1/song/', data, format='json')
        song_id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # create playlist
        data = {
            'name': 'New_Playlist'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + AddSongToPlaylistTest.token)
        response = self.client.post('/api/v1/playlist/', data, format='json')
        playlist_id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # connecting
        response = self.client.post(f'/api/v1/song/{song_id}/add/{playlist_id}/')
        self.assertTrue('ok' in response.data)

        # disconnecting
        response = self.client.post(f'/api/v1/song/{song_id}/remove/{playlist_id}/')
        self.assertTrue('ok' in response.data)


class SearchTest(TestCase):
    def test_search(self):
        query = 'Rammstein'
        response = self.client.get(f'/api/v1/search/{query}')
        self.assertTrue(response.data.get(0, False))


class DownloadingTest(TestCase):
    def test_downloading(self):
        url = "https://cs10-1v4.vkuseraudio.net/s/v1/acmp/iQEz3c0uCAJa0X5kOv1Is1a1gFVSAkBKZW27EDv2453mcNd-2geuTFDxMzNwYRl53BJCNBooYeWW8bWGjB-Z6sP7Nl7LacxGtkxlOPCLxqiuDuQSTX8f4B0rmUhXLehO_5r9Scr6pFOe9L0rq20g5anhQN401x0XtKbOGTY1klPlr_5PtQ.mp3"
        response = self.client.get(f'/api/v1/proxy/?url={url}')
        self.assertTrue(response.status_code, status.HTTP_200_OK)

        with open('test_song.mp3', 'wb') as f:
            f.write(response.content)

        file_size = os.path.getsize('test_song.mp3')
        # размер тестовой песни в байтах
        self.assertEqual(file_size, 9213954)
        os.remove('test_song.mp3')

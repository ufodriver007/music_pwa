from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from main.models import SocialProfile, Playlist, Song


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password"]


class SocialProfileSerializer(ModelSerializer):
    class Meta:
        model = SocialProfile
        fields = '__all__'


class SongSerializer(ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class PlaylistSerializer(ModelSerializer):
    songs = SongSerializer(many=True, required=False)

    class Meta:
        model = Playlist
        fields = '__all__'

    def create(self, validated_data):
        # songs = validated_data.pop('songs', None)
        playlist = Playlist.objects.create(**validated_data)
        return playlist

    def update(self, instance, validated_data):
        songs_data = validated_data.pop('songs', None)       # Извлекаем данные о песнях
        instance = super().update(instance, validated_data)  # Обновляем родительский экземпляр плейлиста

        if songs_data is not None:
            songs = list(instance.songs.all())

            for song_data in songs_data:
                if songs:
                    song = songs.pop(0)
                    song.name = song_data.get('name', song.name)
                    song.author = song_data.get('author', song.author)
                    song.album = song_data.get('album', song.album)
                    song.bitrate = song_data.get('bitrate', song.bitrate)
                    song.duration_text = song_data.get('duration_text', song.duration_text)
                    song.duration = song_data.get('duration', song.duration)
                    song.album_cover_url = song_data.get('album_cover_url', song.album_cover_url)
                    song.url = song_data.get('url', song.url)
                    song.save()

        return instance

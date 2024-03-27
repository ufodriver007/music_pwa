from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from main.models import Profile, Playlist, Song


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password"]


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
        songs = validated_data.pop('songs', None)
        playlist = Playlist.objects.create(**validated_data)

        if songs:
            for song in songs:
                Playlist.songs.add(song)

        return playlist

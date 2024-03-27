from django.contrib import admin
from main.models import Profile, Playlist, Song


@admin.register(Profile)
class MUserAdmin(admin.ModelAdmin):
    list_display = ("user", "description")
    search_fields = ("user", "description")


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ["name", "user"]
    search_fields = ["name", "songs", "user"]
    list_filter = ["name", "user"]


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["name", "author", "album"]
    search_fields = ["name", "author", "album", "bitrate", "duration"]
    list_filter = ("name", "author", "album", "bitrate", "duration")

from django.contrib import admin
from main.models import SocialProfile, Playlist, Song


@admin.register(SocialProfile)
class MUserAdmin(admin.ModelAdmin):
    list_display = ("user", "social_id")
    search_fields = ("user", "social_id")


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

from django.contrib import admin
from main.models import SocialProfile, Playlist, Song
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
import logging


admin_logger = logging.getLogger("admin")


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


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    client_ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('HTTP_X_REAL_IP')
    admin_logger.warning(f"Неудачная попытка входа в админку c IP {client_ip}; username: {request.POST.get('username')}; password: {request.POST.get('password')}.")

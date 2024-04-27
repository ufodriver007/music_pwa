from django.db import models
from django.contrib.auth.models import User


class SocialProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=250, blank=True)
    social_id = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return f'{self.social_id}'

    class Meta:
        verbose_name = 'Соц. профиль'
        verbose_name_plural = 'Соц. профили'


class Song(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    author = models.CharField(max_length=200, verbose_name='Исполнитель', blank=True, null=True)
    album = models.CharField(max_length=200, verbose_name='Альбом', blank=True, null=True)
    bitrate = models.CharField(max_length=200, verbose_name='BitRate', blank=True, null=True)
    duration_text = models.CharField(max_length=200, verbose_name='Длительность', blank=True, null=True)
    duration = models.CharField(max_length=200, verbose_name='Длительность сек.', blank=True, null=True)
    album_cover_url = models.CharField(max_length=250, verbose_name='Обложка альбома', blank=True, null=True)
    url = models.CharField(max_length=250, verbose_name='URL песни')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.author}'

    class Meta:
        verbose_name = 'Песня'
        verbose_name_plural = 'Песни'


class Playlist(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    songs = models.ManyToManyField(Song, verbose_name="Песни")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Плейлист'
        verbose_name_plural = 'Плейлисты'

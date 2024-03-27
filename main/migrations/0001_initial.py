# Generated by Django 5.0.2 on 2024-02-23 09:12

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('description', models.CharField(max_length=200, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('author', models.CharField(max_length=200, verbose_name='Исполнитель')),
                ('album', models.CharField(max_length=200, verbose_name='Альбом')),
                ('bitrate', models.CharField(max_length=200, verbose_name='BitRate')),
                ('duration_text', models.CharField(max_length=200, verbose_name='Длительность')),
                ('duration', models.CharField(max_length=200, verbose_name='Длительность сек.')),
                ('album_cover_url', models.CharField(max_length=250, verbose_name='Обложка альбома')),
                ('url', models.CharField(max_length=250, verbose_name='URL песни')),
            ],
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.muser')),
                ('songs', models.ManyToManyField(to='main.song', verbose_name='Песни')),
            ],
        ),
    ]

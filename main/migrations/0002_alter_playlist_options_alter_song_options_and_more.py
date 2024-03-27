# Generated by Django 5.0.2 on 2024-02-23 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playlist',
            options={'verbose_name': 'Плейлист', 'verbose_name_plural': 'Плейлисты'},
        ),
        migrations.AlterModelOptions(
            name='song',
            options={'verbose_name': 'Песня', 'verbose_name_plural': 'Песни'},
        ),
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.CharField(blank=True, max_length=200, verbose_name='Альбом'),
        ),
        migrations.AlterField(
            model_name='song',
            name='album_cover_url',
            field=models.CharField(blank=True, max_length=250, verbose_name='Обложка альбома'),
        ),
        migrations.AlterField(
            model_name='song',
            name='author',
            field=models.CharField(blank=True, max_length=200, verbose_name='Исполнитель'),
        ),
        migrations.AlterField(
            model_name='song',
            name='bitrate',
            field=models.CharField(blank=True, max_length=200, verbose_name='BitRate'),
        ),
        migrations.AlterField(
            model_name='song',
            name='duration',
            field=models.CharField(blank=True, max_length=200, verbose_name='Длительность сек.'),
        ),
        migrations.AlterField(
            model_name='song',
            name='duration_text',
            field=models.CharField(blank=True, max_length=200, verbose_name='Длительность'),
        ),
    ]

"""
URL configuration for music_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from main.views import UserViewSet, PlaylistViewSet, SongViewSet, SearchView, IndexView, ConnectSongAndPlaylistView, RemoveConnectSongAndPlayView
from django.views.generic import TemplateView


router = SimpleRouter()
router.register(r'api/v1/user', UserViewSet)
router.register(r'api/v1/playlist', PlaylistViewSet)
router.register(r'api/v1/song', SongViewSet)


urlpatterns = [
    path('api/v1/song/<int:song_id>/add/<int:playlist_id>/', ConnectSongAndPlaylistView.as_view()),
    path('api/v1/song/<int:song_id>/remove/<int:playlist_id>/', RemoveConnectSongAndPlayView.as_view()),
    path('api/v1/search/<str:q>', SearchView.as_view()),
    path(r'api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('admin/', admin.site.urls),

    re_path(r'^manifest\.json$', TemplateView.as_view(template_name="main/manifest.json", content_type="application/json")),
    re_path(r'^sw\.js$', TemplateView.as_view(template_name="main/sw.js", content_type="application/javascript")),
    re_path(r'^sw-toolbox\.js$', TemplateView.as_view(template_name="main/sw-toolbox.js", content_type="application/javascript")),

    path('', IndexView.as_view()),
]
urlpatterns += router.urls

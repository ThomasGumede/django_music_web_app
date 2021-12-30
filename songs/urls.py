from django.urls import path
from .views import (AlbumDetailView, Dashboard, SongListView, AlbumListView, SongDetailView, 
SongsAlbumListView, SongCreateView, AlbumCreateView, SongUpdateView, AlbumUpdateView, MusicDeleteView, AlbumDeleteView)

app_name = 'songs'

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('songs', SongListView.as_view(), name='songs'),
    path('albums', AlbumListView.as_view(), name='albums'),
    
    path('song_create', SongCreateView.as_view(), name='song_create'),
    path('album_create', AlbumCreateView.as_view(), name='album_create'),

    path('album_details/<pk>', AlbumDetailView.as_view(), name='album_details'),
    path('song/<pk>', SongDetailView.as_view(), name='song_details'),
    path('songs/<pk>', SongsAlbumListView.as_view(), name='songs_album'),
    path('song_create/<pk>', SongCreateView.as_view(), name='album_song_create'),

    path('album_update/<pk>', AlbumUpdateView.as_view(), name='update_album'),
    path('song_update/<pk>', SongUpdateView.as_view(), name='update_song'),

    path('album_delete/<pk>', AlbumDeleteView.as_view(), name='delete_album'),
    path('song_delete/<pk>', MusicDeleteView.as_view(), name='delete_song'),
]

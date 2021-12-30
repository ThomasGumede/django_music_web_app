from django.contrib import admin
from .models import Album, Music

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('album_title', 'album_genre')

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'duration')

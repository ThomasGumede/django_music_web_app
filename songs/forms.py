from django import forms
from .models import Album, Music

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['album_title', 'album_genre', 'album_cover']

class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['artist', 'title', 'cover', 'audio_file']
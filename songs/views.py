from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from .models import Album, Music
from django.views.generic import DetailView, CreateView, View, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import MusicForm, AlbumForm
from django.urls import reverse, reverse_lazy

class Dashboard(LoginRequiredMixin, View):
    template_name = 'dashboard/dashboard.html'

    def get(self, request):
        user_album = get_list_or_404(Album, album_artist=request.user)
        user_songs = get_list_or_404(Music, owner=request.user, is_single=True)

        return render(request, self.template_name, {'user_album': user_album, 'user_songs': user_songs})

class SongListView(LoginRequiredMixin, ListView):
    template_name = 'music/songs.html'
    model = Music
    context_object_name = 'songs'

class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'music/albums.html'
    context_object_name = 'albums'

class SongsAlbumListView(LoginRequiredMixin, ListView):
    template_name = 'music/songs.html'
    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = get_object_or_404(self.model, pk=self.kwargs['pk'])
        context['songs'] = Music.objects.filter(album=album)
        return context

class AlbumDetailView(LoginRequiredMixin, DetailView):
    model = Album
    template_name = 'music/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        songs = Music.objects.filter(album=self.get_object())
        if songs.exists():
            context['songs_in_album'] = songs
    
        if self.request.user == self.get_object().album_artist:
            context['add_song'] = reverse('songs:album_song_create', kwargs={'pk': self.get_object().pk})
            context['edit_link'] = reverse('songs:update_album', kwargs={'pk': self.get_object().pk})
            context['delete_link'] = reverse('songs:delete_album', kwargs={'pk': self.get_object().pk})
        return context 

class SongDetailView(LoginRequiredMixin, DetailView):
    model = Music
    template_name = 'music/song_detail.html'
    context_object_name = 'song'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user == self.get_object().owner:
            context['edit_link'] = reverse('songs:update_song', kwargs={'pk': self.get_object().pk})
            context['delete_link'] = reverse('songs:delete_song', kwargs={'pk': self.get_object().pk})
        return context

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    template_name = 'music/album_form.html'

    def form_valid(self, form):
        form.instance.album_artist = self.request.user
        form.save()
        return super().form_valid(form)

class SongCreateView(LoginRequiredMixin, View):
    model = Music
    form_class = MusicForm
    template_name = 'music/song_form.html'
    album = None

    def get(self, request, pk=None, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, pk=None, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            if pk is not None:
                self.album = get_object_or_404(Album, pk=pk)
                form.album = self.album
            form.save()
            return redirect('songs:songs')
        else:
            return render(request, self.template_name, {'form': self.form_class})

class AlbumUpdateView(LoginRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    template_name = 'music/album_form.html'

class SongUpdateView(LoginRequiredMixin, UpdateView):
    model = Music
    form_class = MusicForm
    template_name = 'music/song_form.html'

class MusicDeleteView(LoginRequiredMixin, DeleteView):
    model = Music
    template_name = 'music/confirm_delete.html'
    success_url = reverse_lazy('songs:songs')

class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    model = Album
    template_name = 'music/confirm_delete.html'
    success_url = reverse_lazy('songs:albums')
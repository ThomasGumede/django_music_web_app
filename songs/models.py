from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from utils.helper import get_audio_length
from utils.validators import validate_is_audio
from django.urls import reverse
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
User = get_user_model()

# Create your models here.
class Album(models.Model):
	album_artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
	album_title = models.CharField(max_length=300)
	album_genre = models.CharField(max_length=30)
	album_cover = models.ImageField(upload_to='album_covers/')
	uploaded_on = models.DateField(default=timezone.now)

	def __str__(self) -> str:
		return f"{self.album_title}"

	def get_absolute_url(self):
		return reverse('songs:album_details', kwargs={"pk": self.pk})
	

class Music(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)
	artist = models.CharField(max_length=300)
	title = models.CharField(max_length=300)
	duration=models.DecimalField(max_digits=20, decimal_places=2,blank=True)
	cover = models.ImageField(upload_to='song_covers/')
	is_single = models.BooleanField(default=False)
	audio_file = models.FileField(upload_to='musics/',validators=[validate_is_audio])
	uploaded_on = models.DateField(default=timezone.now)

	def __str__(self) -> str:
		return self.title

	def get_absolute_url(self):
		return reverse('songs:song_details', kwargs={"pk": self.pk})
	
	def save(self, *args, **kwargs):
		if not self.album:
			self.is_single = True
		
		if not self.duration:
			duration_time = get_audio_length(self.audio_file)
			self.duration = f'{duration_time:.2f}'
	   
		return super(Music, self).save(*args, **kwargs)

# Signals for deleting object file from memory disk
@receiver(pre_delete, sender=Music)
def delete_image_audio_hook(sender, instance, using, **kwargs):
	instance.cover.delete()
	instance.audio_file.delete()
	

@receiver(pre_delete, sender=Album)
def delete_image_hook(sender, instance, using, **kwargs):
	instance.album_cover.delete()
	

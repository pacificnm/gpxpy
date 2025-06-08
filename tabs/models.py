from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Artist Model
class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
# Album Model
class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.artist.name}-{self.title}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.artist.name} – {self.title}"
    
# Song model
class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    mp3_file = models.FileField(upload_to='media_root/tracks/')
    gpx_file = models.FileField(upload_to='media_root/gpx/', blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_songs')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.album.artist.name}-{self.album.title}-{self.title}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.album.artist.name} – {self.album.title})"
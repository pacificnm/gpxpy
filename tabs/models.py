from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from .utils.id3_utils import extract_id3_metadata  # Make sure this exists


# Genre
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
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
    
# Song
class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    mp3_file = models.FileField(upload_to='tracks/')
    gpx_file = models.FileField(upload_to='gpx/', blank=True, null=True)
    artwork = models.ImageField(upload_to='artwork/', blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='songs', blank=True)
    track_number = models.PositiveIntegerField(blank=True, null=True)
    gpx_synced = models.BooleanField(default=False)  # New sync flag
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='uploaded_songs')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding and not self.pk
        meta = None

        # Initial save to store the file on disk
        super().save(*args, **kwargs)

        if is_new and self.mp3_file:
            # temp set flag to true
            self.gpx_synced = True
            
            # Fetch meta
            meta = extract_id3_metadata(self.mp3_file.path)

            if meta:
                self.title = meta.get('title') or self.title
                self.track_number = meta.get('track_num')
                self.year = meta.get('year') or self.year
                self.track_number = meta.get('track_num') or self.track_number

                if meta.get('artwork_file'):
                    self.artwork.save('cover.jpg', meta['artwork_file'], save=False)

                # Create slug if missing (after we have the title)
                if not self.slug:
                    self.slug = slugify(f"{self.album.artist.name}-{self.album.title}-{self.title}")

                # Save again only if we updated metadata
                super().save(update_fields=["title", "track_number", "slug", "artwork"])

                # Add genres
                if meta.get('genres'):
                    for genre_name in meta['genres']:
                        genre_obj, _ = Genre.objects.get_or_create(name=genre_name)
                        self.genres.add(genre_obj)

    # return the saved data
    def __str__(self):
        return f"{self.title} ({self.album.artist.name} – {self.album.title})"

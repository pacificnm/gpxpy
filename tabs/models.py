from django.db import models
from django.utils.text import slugify

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
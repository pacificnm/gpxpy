from django.contrib import admin
from .models import Artist
from .models import Album
from .models import Song
from .models import Genre

# Artist
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")

# Album
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("artist", "title", "slug")

# Song
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "album", "uploaded_by", "uploaded_at")

# Genre
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)
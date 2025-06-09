from django.contrib import admin
from django.utils.html import format_html
from .models import Song, Genre, Album, Artist

class AlbumInline(admin.TabularInline):  # Or use StackedInline for a different look
    model = Album
    fields  = ("artwork_thumbnail", "artist", "title", "slug", "track_count")
    readonly_fields = ("artwork_thumbnail", "track_count")
    extra = 0  # No empty extra forms
    show_change_link = True  # Adds a link to the Album edit page

    def artwork_thumbnail(self, obj):
        song_with_art = obj.songs.filter(artwork__isnull=False).first()
        if song_with_art and song_with_art.artwork:
            return format_html('<img src="{}" width="60" />', song_with_art.artwork.url)
        return "(no artwork)"
    artwork_thumbnail.short_description = "Artwork"

    def track_count(self, obj):
        return obj.songs.count()
    track_count.short_description = "Tracks"
    

# Actions
@admin.action(description="Toggle GPX Synced")
def toggle_gpx_synced(modeladmin, request, queryset):
    for song in queryset:
        song.gpx_synced = not song.gpx_synced
        song.save()


# Artist
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug", "album_count")
    inlines = [AlbumInline]

    # define album count
    def album_count(self, obj):
        return obj.albums.count()

    album_count.short_description = 'Albums'

# Album
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("artwork_thumbnail", "artist", "title", "slug", "track_count")

    def artwork_thumbnail(self):
        song_with_art = self.songs.filter(artwork__isnull=False).first()
        if song_with_art and song_with_art.artwork:
            return format_html('<img src="{}" width="60" />', song_with_art.artwork.url)
        return "(no artwork)"
    
    artwork_thumbnail.short_description = "Artwork"

    def track_count(self):
        return self.songs.count()
    
    track_count.short_description = "Tracks"

# Song
@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'album', 'uploaded_by', 'uploaded_at', 'gpx_synced')
    actions = [toggle_gpx_synced]

# Genre
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ('name',)
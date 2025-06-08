from django.contrib import admin
from .models import Artist

# Artist
@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")

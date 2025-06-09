from django.shortcuts import render
from .models import Song

# tabs/views.py
def home(request):
    newest_songs = Song.objects.order_by('-uploaded_at')[:10]
    most_played_songs = Song.objects.order_by('-play_count')[:10]

    return render(request, 'home.html', {
        'newest_songs': newest_songs,
        'most_played_songs': most_played_songs
    })

def profile_view(request):
    return render(request, 'profile.html')

def favorites_view(request):
    return render(request, 'favorites.html')

def setlists_view(request):
    return render(request, 'setlists.html')

def logout(request):
    return render(request, 'logout.html')
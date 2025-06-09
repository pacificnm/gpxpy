from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
     path('profile/', views.profile_view, name='profile'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('setlists/', views.setlists_view, name='setlists'),
     path('logout/', views.setlists_view, name='logout'),
]

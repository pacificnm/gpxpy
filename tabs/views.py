from django.shortcuts import render
from django.http import HttpResponse

# tabs/views.py
def home(request):
    return render(request, 'tabs/home.html')

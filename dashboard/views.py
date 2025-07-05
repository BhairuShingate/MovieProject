from django.shortcuts import render
from movies.models import Movie
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.

# @login_required

def homeview(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'dashboard/home_main.html', context) 
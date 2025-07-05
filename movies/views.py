from django.shortcuts import render,redirect
# Create your views here.
from .models import Movie
from reviews.models import Review
from django.db.models import Count, Avg
from datetime import date
from django.contrib import messages


def movie_detail(request, slug):
    movie = Movie.objects.get(slug=slug)
    reviews = Review.objects.filter(movie=movie).select_related('user').order_by('-created_at')
    review_stats = reviews.aggregate(
        total_reviews=Count('id'),
        avg_rating=Avg('rating'),
    )
    today_date = date.today().strftime('%Y-%m-%d')
    return render(request, 'movies/movie_main.html', {'movie': movie,'reviews': reviews,'review_stats': review_stats,'today_date': today_date})

  # Adjust based on your app/model

def search_movies(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.filter(title__icontains=query) if query else []

    for movie in movies:
        print(movie.title, movie.slug)  # ✅ Check slug values in console

    context = {
        'movies': movies,
        'query': query,
    }
    return render(request, 'movies/search_results.html', context)


from django.urls import path
from . import views

urlpatterns = [
    path('movie/<slug>/', views.movie_detail, name='movie_detail'),
    path('movies/search/', views.search_movies, name='search_movies'),
]

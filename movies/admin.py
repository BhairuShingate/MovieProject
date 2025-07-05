from django.contrib import admin
from .models import Movie,Cast

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'release_date', 'status','synopsis', 'duration_minutes', 'movie_image','trailer_url', 'created_at')
    
@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ('movie', 'name', 'role', 'image')    
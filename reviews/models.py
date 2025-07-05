from django.db import models
from accounts.models import User
from movies.models import Movie
# Create your models here.

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=0, choices=[(i, str(i)) for i in range(1, 6)],null=True, blank=True)
    review_text = models.TextField(null=True, blank=True)
    # comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.movie.title}'
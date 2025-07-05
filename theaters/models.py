from django.db import models
from movies.models import Movie 
# Create your models here.
class Theater(models.Model):
    name = models.CharField(max_length=1000)
    city = models.CharField(max_length=250)
    address = models.TextField(max_length=255)

    def __str__(self):
        return f'{self.name} - {self.city}'
    
choices=[
    ('regular', 'Regular'),
    ('silver', 'Silver'),
    ('gold', 'Gold'),
]

class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.IntegerField()
    row_label = models.CharField(max_length=1)
    seat_type = models.CharField(max_length=50, choices=choices, default='Regular')
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f'Seat {self.seat_number} in {self.theater.name}'
    
class Showtime(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    movie= models.ForeignKey(Movie,on_delete=models.CASCADE)
    showtime = models.DateTimeField()
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    silver_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gold_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.movie} at {self.showtime} in {self.theater.name}'  
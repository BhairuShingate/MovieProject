from django.contrib import admin
from .models import Booking,Bookingseat

# Register your models here.
@admin.register(Booking)
class UserAdmin(admin.ModelAdmin):  
    list_display = ['user', 'showtime', 'booking_time', 'status', 'total_amount']

@admin.register(Bookingseat)
class UserAdmin(admin.ModelAdmin):  
    list_display = ['booking','seat','showtime']
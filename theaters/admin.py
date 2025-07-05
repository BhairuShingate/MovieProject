from django.contrib import admin
from .models import Theater,Seat,Showtime
# Register your models here.

@admin.action(description="Generate Silver, Gold, Recliner seats")
def generate_all_seats(modeladmin, request, queryset):
    seat_plan = {
        'regular': {
            'rows': ['A', 'B', 'C'],
            'seats_per_row': 10
        },
        'silver': {
            'rows': ['D', 'E'],
            'seats_per_row': 8
        },
        'gold': {
            'rows': ['F'],
            'seats_per_row': 6
        }
    }

    for theater in queryset:
        for seat_type, config in seat_plan.items():
            for row in config['rows']:
                for seat_number in range(1, config['seats_per_row'] + 1):
                    Seat.objects.get_or_create(
                        theater=theater,
                        row_label=row,
                        seat_number=seat_number,
                        seat_type=seat_type
                    )
        modeladmin.message_user(request, f"Seats added for {theater.name}")

@admin.register(Theater)
class AdminTheater(admin.ModelAdmin):
    list_display = ['name','city','address']
    ordering = ['name']
    actions = [generate_all_seats]

@admin.register(Seat)
class AdminSeat(admin.ModelAdmin):
    list_display = ['theater','row_label','seat_number','seat_type']
    ordering = ['theater']

@admin.register(Showtime)
class AdminShowtime(admin.ModelAdmin):
    list_display = ['theater', 'movie', 'showtime', 'regular_price', 'silver_price', 'gold_price']
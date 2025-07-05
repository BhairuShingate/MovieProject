from django.shortcuts import render,redirect
from theaters.models import Theater, Showtime
from movies.models import Movie
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime
from datetime import datetime, timedelta
from django.utils import timezone
from theaters.models import Showtime
from theaters.models import Seat
from django.contrib.auth.decorators import login_required
import json
from accounts.models import User
from bookings.models import Booking,Bookingseat
from django.conf import settings


def Theater_Showtime_view(request, slug, date_str):
    if not Movie.objects.filter(slug=slug).exists():
        messages.error(request, 'Invalid request')
        return render(request, 'theaters/showtimes.html', {})

    movie = Movie.objects.get(slug=slug)
    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()

    showtimes = Showtime.objects.filter(movie=movie, showtime__date=selected_date)

    date_range = [selected_date + timedelta(days=i) for i in range(7)]

    all_showtimes = Showtime.objects.filter(movie=movie)
    available_dates = set(show.showtime.date() for show in all_showtimes)
    current_datetime = timezone.now()

    context = {
        'movie': movie,
        'showtimes': showtimes,
        'date_str': date_str,
        'date_range': date_range,
        'available_dates': available_dates,
        'current_datetime': current_datetime,
    }
    return render(request, 'theaters/showtime.html', context)


def seats_view(request, show_id):
    showtime = Showtime.objects.get(id=show_id)
    theater = showtime.theater
    movie = showtime.movie
    seats = Seat.objects.filter(theater=theater).order_by('-row_label', 'seat_number')

    seat_rows = {}
    booked_seats = [booking_seat.seat for booking_seat in Bookingseat.objects.filter(showtime=showtime)]  # You can replace this with actual booked seats logic

    for s in seats:
        seat_type = s.seat_type.lower()  # ✅ Normalize seat type to lowercase
        row = (s.row_label, seat_type)
        if row not in seat_rows:
            seat_rows[row] = []
        if s not in booked_seats:
            seat_rows[row].append(s)
        else:
            seat_rows[row].append(0)

    seat_categories = [
        {'type': 'regular', 'price': showtime.regular_price},
        {'type': 'silver', 'price': showtime.silver_price},
        {'type': 'gold', 'price': showtime.gold_price},
    ]


    context = {
        'movie': movie,
        'theater': theater,
        'seats': seats,
        'showtime': showtime,
        'seat_rows': seat_rows,
        'seat_categories': seat_categories,
    }
    return render(request, 'theaters/seats.html', context)


@login_required
def Book_Ticket_view(request, show_id):
    if request.method == 'POST':
        selected_seats_json = request.POST.get('selected_seats')
        total_amount = float(request.POST.get('total_amount'))

        if not selected_seats_json or not total_amount:
            messages.error(request, "Please select seats and try again.")
            return redirect('seats_view', show_id=show_id)


        selected_seats = json.loads(selected_seats_json)

        showtime = Showtime.objects.get(id=show_id)
        convenience_fee = float(total_amount) * 0.10
        final_amount = total_amount+ convenience_fee

        booking = Booking.objects.create(
            user=request.user,
            showtime=showtime,
            total_amount=final_amount
        )
        booked_seat_numbers=[]
        for seat_data in selected_seats:
                seat_id = int(seat_data['id'])  
                seat = Seat.objects.get(id=seat_id)

                if seat.is_booked:
                    continue

                Bookingseat.objects.create(booking=booking, seat=seat, showtime=showtime)
                seat.is_booked = True
                seat.save()
                booked_seat_numbers.append(seat.seat_number)
        context={
            'selected_seats':booked_seat_numbers,
            'booking':booking,
            'total_amount':total_amount,
            'convenience_fee':convenience_fee,
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY
            
        }

        return render(request,'bookings/payment.html',context)

    return HttpResponse("Invalid request")


@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related(
        'showtime__movie',
        'showtime__theater',
    ).prefetch_related(
        'bookingseat_set__seat'
    ).order_by('-booking_time')

    movie_title = request.GET.get('movie')
    if movie_title:
        bookings = bookings.filter(showtime__movie__title__icontains=movie_title)

    return render(request, 'bookings/order_details.html', {'bookings': bookings})

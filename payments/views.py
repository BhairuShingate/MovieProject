from django.shortcuts import render,redirect
from bookings.models import Booking
from payments.models import Payment
from accounts.models import User
from django.conf import settings
from django.http import HttpResponse
import stripe
stripe.api_key=settings.STRIPE_SECRET_KEY
# Create your views here.

def  payment_view(request,booking_id):
    booking=Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        # Create a Stripe Checkout session
        session = stripe.checkout.Session.create (
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': f'Ticket Booking',
                        },
                        'unit_amount':int(booking.total_amount * 100),  # Amount in cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            billing_address_collection='required',
            success_url=f'http://127.0.0.1:8000/payment/success/{booking_id}/',
            cancel_url=f'http://127.0.0.1:8000/payment/error/{booking_id}/'
        )
        return  redirect(session.url,code=303)
    return render(request, 'bookings/booking_summary.html',{
        'booking':booking,
        'stripe_public_key':settings.STRIPE_PUBLIC_KEY,
    } )       
       
def Success_view(request,booking_id):
    booking=Booking.objects.get(id=booking_id)
    booking.status='booked'
    booking.save()
    Payment.objects.create(
        booking=booking,
        amount=booking.total_amount,
        payment_method='card',
        status='successful'
    )
    return render(request,'payments/success.html')

def Cancel_view(request,booking_id):
    booking=Booking.objects.get(id=booking_id)
    booking.status='canceled'
    booking.save()
    Payment.objects.create(
        booking=booking,
        amount=booking.total_amount,
        payment_method='card',
        status='failed'
    )
    return render(request,'payments/error.html')

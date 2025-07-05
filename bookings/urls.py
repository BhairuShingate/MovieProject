from django.urls import path
from . import views 
urlpatterns = [
    path('showtime/<slug:slug>/<str:date_str>/', views.Theater_Showtime_view, name='Theater_Showtime'),
    path('seats/<int:show_id>/', views.seats_view, name='seats_view'),
    path('book/<int:show_id>/', views.Book_Ticket_view, name='book'),
    path('order/', views.view_bookings, name='order'),

    
]
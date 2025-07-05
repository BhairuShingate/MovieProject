from django.urls import path
from . import views

urlpatterns = [
    path('payments/<int:booking_id>/', views.payment_view, name='payments'),
    path('success/<int:booking_id>/', views.Success_view, name='success'),
    path('cancel/<int:booking_id>/', views.Cancel_view, name='cancel'),
    
]

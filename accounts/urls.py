from django.urls import path
from . import views 
urlpatterns = [
    path('Register/',views.RegisterView,name='Register'),
    path('Login/',views.LoginView,name='Login'),
    path('Home',views.HomeView,name='Home'),
    path('Logout/',views.LogoutView,name='Logout'),
    path('IdentityUser/', views.IdentityUserView, name='IdentityUser'),
    path('otp/<str:en_uname>/', views.OTPView, name='otp'),
    path('resetpassword/<str:en_uname>/',views.ResetPasswordView, name='resetpassword'),

]
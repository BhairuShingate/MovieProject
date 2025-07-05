from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms  import RegisterForm, LoginForm
from django.core.mail import send_mail
from .models import User
from .forms import IdentityForm
from django.utils import timezone
import datetime
from .utils import get_otp, enc_uname, dec_uname
from django.contrib.auth.forms import SetPasswordForm

from django.urls import reverse
from movies.models import Movie
from django.urls import reverse


# Create your views here.

def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            fname=form.cleaned_data['first_name']
            lname=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            
            send_mail(
                'registration successfull',
                'Hello '+fname+' '+lname+', \n\nyou have successfully registered with us. \n\nThank you for registering with us.',
                'bhairushingate749@gmail.com',
                [email],
                fail_silently=True,
            )
            return redirect('Login')  # Redirect to the login page after successful registration
            # return HttpResponse('Registration successful! A confirmation email has been sent to your email address.')
    else:
        form = RegisterForm()  
    return render(request, 'accounts/register.html', {'form': form})



def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('Home')  
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


# @login_required
def HomeView(request):
    # return render(request,'accounts/home.html')
    movies = Movie.objects.all()
    return render(request, 'dashboard/home_main.html', {'movies':movies})

# @login_required(login_url='Login')
def LogoutView(request):                                                                                                                                                                                            
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('Login')  # Redirect to the login page after logout

def IdentityUserView(request):
    if request.method=='POST':
        form=IdentityForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username) 
                otp=get_otp()
                time=timezone.now() + datetime.timedelta(minutes=10)
                user.otp=otp
                user.otp_expired=time
                user.otp_verified=False
                email=user.email
                user.save()
                send_mail(
                    'OTP for Identity Verification',
                    f'Your OTP is {otp}. enter otp to reset your password. \n\nThis OTP is valid for 10 minutes.',
                    'bhairushingate749@gmail.com',
                    [email],
                    fail_silently=True,
                )
                messages.success(request, 'user found otp has sent to registered email.')
                en_uname=enc_uname(username)
                url=f'/accounts/otp/{en_uname}/'
                return redirect(url)
            messages.error(request, 'user not found.')
    context={
        'form': IdentityForm()
    }
    return render(request,'accounts/identity.html',context)



def OTPView(request,en_uname):
    username = dec_uname(en_uname)
    if User.objects.filter(username=username).exists():
        if request.method == 'POST':
            otp = int(request.POST.get('otp'))
            user = User.objects.get(username=username)
            if timezone.now() <= user.otp_expired:
                if not user.otp_verified:
                    if user.otp == otp:
                        user.otp_verified = True
                        user.save()
                        messages.success(request, 'OTP verified successfully.')
                        url=f'/accounts/resetpassword/{en_uname}/'
                        return redirect(url)
                    else:
                        messages.error(request, 'Invalid OTP. Please try again.')
                        return redirect('IdentifyUser')
                messages.error(request, 'OTP already verified.')
                return redirect('IdentityUser')
            messages.error(request, 'OTP has expired. Please request a new OTP.')
            return redirect('otp', en_uname=en_uname)
        return render(request, 'accounts/otp.html')
    messages.error(request, 'Invalid request.')
    return redirect('Login')

def ResetPasswordView(request,en_uname ):
    try:
        Username = dec_uname(en_uname)
    except:
        messages.error(request, 'Invalid username.')
        return redirect('Login')
    if User.objects.filter(username=Username).exists():
        user = User.objects.get(username=Username)
        if request.method == 'POST':
            form = SetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                messages.success(request, 'Password reset successfully.')
                form.save()
                return redirect('Login')
            else:
                messages.error(request, 'Please correct the errors below.')
        context = {
            'form' : SetPasswordForm(user=user)
        }
        return render(request, 'accounts/reset_password.html', context)
    messages.error(request, 'invalid requiest.')
    return redirect('Login')
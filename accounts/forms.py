# from django import forms
# from django.contrib.auth.forms import (UserCreationForm,
#                                        AuthenticationForm)

# from .models import User

# class RegisterForm(UserCreationForm):
#     class Meta:
#         model=User
#         fields=('first_name','last_name','username','email','phone','password1','password2')

#         widget={
#             'first_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'First name'
#             }),
#             'last_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Last name'
#             }),
#             'username': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Username'
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Email address'
#             }),
#             'phone': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Phone number'
#             }),
#             'password1': forms.PasswordInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Password'
#             }),
#             'password2': forms.PasswordInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Confirm password'
#             })
#         }
    


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Phone Number'}),
        }

    def _init_(self, *args, **kwargs):
        super(RegisterForm, self)._init_(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'input-field', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'input-field', 'placeholder': 'Confirm Password'})


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )

class IdentityForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
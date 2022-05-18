from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from .models import Useradd

class SignUpForm(UserCreationForm):
    first_name = forms.CharField( label = "Enter Firstname", widget = forms.TextInput(attrs = {'class' : 'form-control'}))
    last_name = forms.CharField( label = "Enter Lastname", widget = forms.TextInput(attrs = {'class' : 'form-control'}))
    username = forms.CharField( label = "Enter Username",
     widget = forms.TextInput(attrs = {'class' : 'form-control'}))
    email = forms.CharField(label = "Enter Email",
     widget = forms.EmailInput(attrs = {'class' : 'form-control'}))
    password1 = forms.CharField(
        label = "Password",
        strip = False,
        widget = forms.PasswordInput(attrs = {'autocomplete': 'new-password',
        'class' : 'form-control'}),
    )
    password2 = forms.CharField(
        label = "Confirm Password",
        strip = False,
        widget = forms.PasswordInput(attrs = {'autocomplete' : 'new-password',
        'class' : 'form-control'}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password1", "password2")
     

class LoginForm(AuthenticationForm):
    username = UsernameField(widget = forms.TextInput(attrs = {'autofocus' : True, 'class' : 'form-control'}))
    password = forms.CharField(
        label = 'Enter password',
        strip = False,
        widget = forms.PasswordInput(attrs = {'autocomplete' : 'current-password', 'class' : 'form-control'}),
    )


class AddressForm(forms.ModelForm):
    class Meta:
        model = Useradd
        fields = ('mobile_no',)
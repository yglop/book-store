from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import *


class RegisterForm(UserCreationForm):
    email = forms.EmailField

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class CustomerSettingsForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['profile_pic']


class UserSettingsForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class BookCreationForm(forms.Form):
    name = forms.CharField(max_length=100)
    author = forms.CharField(max_length=100)
    price = forms.FloatField()
    category = forms.CharField(max_length=100)
    description = forms.CharField(max_length=800)
    picture = forms.ImageField()
    book_file = forms.FileField()


class BookRedactionForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'price', 'category', 'description', 'picture', 'book_file']


from django import forms
from matplotlib import widgets
from .models import *


from django.contrib.auth.forms import UserCreationForm




class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username','first_name','last_name','email','password1','password2']
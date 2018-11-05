from django import forms
from django.contrib.auth.models import User
from basicapp.models import *

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    username=forms.CharField(max_length=120)

    class Meta():
        model=User
        fields=("username","email","password")

class UserProfileInfoForms(forms.ModelForm):
    class Meta():
        model=UserProfileInfo
        fields=("portfolio_site","profile_pic")

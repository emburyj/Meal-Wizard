from django import forms
from django.forms import HiddenInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model =  User
        fields = ['username', 'email', 'password1', 'password2']

class UserFollowForm(forms.Form):
    box = forms.BooleanField(widget=HiddenInput(), required=False)
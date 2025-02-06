from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class FortuneTellingForm(forms.Form):
    name = forms.CharField(max_length=100, label='姓名')
    birth_date = forms.DateField(label='出生日期', widget=forms.DateInput(attrs={'type': 'date'}))
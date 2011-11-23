from models import *
from django import forms

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'restaurant_prefs', 'day_prefs')
    name = forms.CharField(max_length=100)
    email = forms.EmailField() 

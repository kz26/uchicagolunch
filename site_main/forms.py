from models import *
from django.forms import Form, ModelForm

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ('restaurant_prefs', 'day_prefs')

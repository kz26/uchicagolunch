from models import *
from django import forms
from validators import *
from datetime import date, timedelta
from django.conf import settings

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'restaurant_prefs', 'day_prefs')
    name = forms.CharField(max_length=100)
    email = forms.EmailField(validators=[uchicago_validate]) 
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        tomorrow = date.today() + timedelta(days=1)
        maxdate = date.today() + timedelta(days=settings.DAYS_IN_FUTURE)
        self.fields['day_prefs'].queryset = Day.objects.filter(date__range=(tomorrow, maxdate))
            

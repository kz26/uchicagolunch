from models import *
from django import forms
from validators import *
from datetime import date, timedelta
from django.conf import settings

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('name', 'email', 'restaurant_prefs', 'day_prefs')
    email = forms.EmailField(label="UChicago email address", validators=[uchicago_validate, banned_check]) 
    day_prefs = forms.TypedMultipleChoiceField(label='When are you available for lunch?', coerce=lambda x: date.fromordinal(int(x)))

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)

        days = []
        for i in range(1, settings.DAYS_IN_FUTURE + 1):
            d = date.today() + timedelta(days=i)
            days.append( (str(d.toordinal()), d.strftime("%A, %B %d")) )

        self.fields['day_prefs'].choices = days
            

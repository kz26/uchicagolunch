from django.core.exceptions import ValidationError
from site_main.models import *
from datetime import datetime
from re import search

def uchicago_validate(value):
   if not search(r'uchicago.edu$', value):
       raise ValidationError("Only @uchicago.edu email addresses are supported at this time.")
   if Request.objects.filter(email=value, matched=False, expires__gt=datetime.now()).exists():
       raise ValidationError("This email address has already been registered for the current scheduling period.")

def banned_check(value):
    if Ban.objects.filter(email=value).exists():
        raise ValidationError("This email address has been banned.")

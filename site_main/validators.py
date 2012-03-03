from django.core.exceptions import ValidationError
from site_main.models import *
from re import search

def uchicago_validate(value):
   if not search(r'uchicago.edu$', value):
       raise ValidationError("Only @uchicago.edu email addresses are supported at this time.")
   if Request.objects.filter(email=value).exists():
       raise ValidationError("This email address has already been registered for the current period.")

def banned_check(value):
    if Ban.objects.filter(email=value).exists():
        raise ValidationError("This email address has been banned.")

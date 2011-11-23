from django.core.exceptions import ValidationError
from models import Person
from re import search

def uchicago_validate(value):
   if not search(r'uchicago.edu$', value):
       raise ValidationError("Only @uchicago.edu email addresses are supported at this time.")
   if Person.objects.filter(email=value).exists():
       raise ValidationError("This email address has already been registered for the current cycle.")

from models import *
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def notify_match(mo): # takes a match object
    subject = r"[UChicago.Lunch] You've got a lunch date!"

    # send to person1
    msg = render_to_string('email.html', {'match': mo})
    e = EmailMessage(subject, msg, settings.DEFAULT_FROM_EMAIL, [mo.person1.email]) 
    e.content_subtype = 'html'
    e.send()

    # send to person2
    msg = render_to_string('email.html', {'match': mo, 'switch': True})
    e = EmailMessage(subject, msg, settings.DEFAULT_FROM_EMAIL, [mo.person2.email])
    e.content_subtype = 'html'
    e.send()

from models import *
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_activation_email(r):
    subject = r"[UChicago.Lunch] Confirm your request"
    msg = render_to_string('email-activate.html', {'req': r}) 
    e = EmailMessage(subject, msg, settings.DEFAULT_FROM_EMAIL, [r.email])
    e.content_subtype = 'html'
    e.send()

def notify_match(mo): # takes a match object
    subject = r"[UChicago.Lunch] You've got a lunch date!"
    fromto = [mo.request1, mo.request2]
    for p in (fromto, fromto[::-1]):
        msg = render_to_string('email-match.html', {'match': mo, 'from': p[0], 'to': p[1]})
        e = EmailMessage(subject, msg, settings.DEFAULT_FROM_EMAIL, [p[1].email]) 
        e.content_subtype = 'html'
        e.send()

def notify_expired(req): # takes a Request object
    subject = r"[UChicago.Lunch] Your request"
    msg = render_to_string('email-expired.html', {'req': req})
    e = EmailMessage(subject, msg, settings.DEFAULT_FROM_EMAIL, [req.email])
    e.content_subtype = 'html'
    e.send()

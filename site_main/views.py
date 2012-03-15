# Create your views here.
from models import *
from django.shortcuts import *
from forms import *
from datetime import date, timedelta, time
from django.conf import settings
from emails import *

WEEK_FORMAT_STR = "%B %d"

def home(request):
    valid_submit = False
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            days = form.cleaned_data['day_prefs']
            r = form.save(commit=False)
            r.expires = datetime.combine(min(days), time(8)) # expire new, unactivated on the earliest selected day, 8am
            r.save()
            form.save_m2m()
            for d in days:
                Day.objects.create(request=r, date=d)
            send_activation_email(r) 
            valid_submit = True
    else:
        form = RequestForm()
    tomorrow = date.today() + timedelta(days=1)
    endday = date.today() + timedelta(days=settings.DAYS_IN_FUTURE)
    weekstr = "%s - %s, %s" % (tomorrow.strftime(WEEK_FORMAT_STR), endday.strftime(WEEK_FORMAT_STR), date.today().year)
    return render(request, 'index.html', dictionary={'weekstr': weekstr, 'form': form, 'valid_submit': valid_submit})

def activate(request, code):
    try:
        r = Request.objects.get(activation_key=code, active=False)
        r.active = True
        rdates = tuple(r.day_set.values_list('date', flat=True))
        r.expires = datetime.combine(max(rdates), time(8)) # set the new expiration date to the lates selected day, 8am
        r.save()
        return render(request, 'activated.html', dictionary={'req': r})
    except:
        return render(request, 'activation_invalid.html')

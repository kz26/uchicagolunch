# Create your views here.
from models import *
from django.shortcuts import *
from forms import *
from datetime import date, timedelta, time
from django.conf import settings
from emailhelper import *

WEEK_FORMAT_STR = "%B %d"

def home(request):
    valid_submit = False
    if request.method == 'POST':
        client = Client()
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            person = Person.objects.get_or_create(email=form.cleaned_data['email'])[0]
            if person.name != form.cleaned_data['name']:
                person.name = form.cleaned_data['name']
                person.save()
            client.person = person
            dates = [d.date for d in form.cleaned_data['day_prefs']]
            client.expires = datetime.combine(min(dates), time(8)) # expire new, unactivated on the earliest selected day, 8am
            form.save()
            send_activation_email(client) 
            valid_submit = True
    else:
        form = ClientForm()
    tomorrow = date.today() + timedelta(days=1)
    endday = date.today() + timedelta(days=settings.DAYS_IN_FUTURE)
    weekstr = "%s - %s, %s" % (tomorrow.strftime(WEEK_FORMAT_STR), endday.strftime(WEEK_FORMAT_STR), date.today().year)
    return render(request, 'index.html', dictionary={'weekstr': weekstr, 'form': form, 'valid_submit': valid_submit})

def activate(request, code):
    try:
        c = Client.objects.get(act_code=code, active=False)
        c.active = True
        cdates = tuple(c.day_prefs.values_list('date', flat=True))
        c.expires = datetime.combine(max(cdates), time(8)) # set the new expiration date to the lates selected day, 8am
        c.save()
        return render(request, 'activated.html', dictionary={'client': c})
    except:
        return render(request, 'activation_invalid.html')

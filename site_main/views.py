# Create your views here.
from models import *
from django.shortcuts import *
from forms import *
from datetime import date, timedelta, time
from django.conf import settings

WEEK_FORMAT_STR = "%B %d"

def home(request):
    valid_submit = False
    if request.method == 'POST':
        client = Client()
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            person = Person.objects.get_or_create(name=form.cleaned_data['name'], email=form.cleaned_data['email'])[0]
            client.person = person
            dates = [d.date for d in form.cleaned_data['day_prefs']]
            client.expires = datetime.combine(max(dates), time(23, 59, 59))
            form.save()
            valid_submit = True
    else:
        form = ClientForm()
    tomorrow = date.today() + timedelta(days=1)
    endday = date.today() + timedelta(days=settings.DAYS_IN_FUTURE)
    weekstr = "%s - %s, %s" % (tomorrow.strftime(WEEK_FORMAT_STR), endday.strftime(WEEK_FORMAT_STR), date.today().year)
    return render(request, 'index.html', dictionary={'weekstr': weekstr, 'form': form, 'valid_submit': valid_submit})

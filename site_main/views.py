# Create your views here.
from models import *
from django.shortcuts import *
from forms import *
from datehelper import *

WEEK_FORMAT_STR = "%B %d"

def home(request):
    valid_submit = False
    if request.method == 'POST':
        client = Client()
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            person = Person.objects.get_or_create(name=form.cleaned_data['name'], email=form.cleaned_data['email'])[0]
            client.person = person
            form.save()
            valid_submit = True
    else:
        form = ClientForm()
    week = getNextWeekNow()
    weekstr = "%s - %s, %s" % (week[0].strftime(WEEK_FORMAT_STR), week[1].strftime(WEEK_FORMAT_STR), datetime.now().year)
    return render(request, 'index.html', dictionary={'weekstr': weekstr, 'form': form, 'valid_submit': valid_submit})

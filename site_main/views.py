# Create your views here.
from models import *
from django.shortcuts import *
from forms import *
from datehelper import *

WEEK_FORMAT_STR = "%B %d"

def home(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
    else:
        form = ClientForm()
    week = getNextWeekNow()
    weekstr = "%s - %s, %s" % (week[0].strftime(WEEK_FORMAT_STR), week[1].strftime(WEEK_FORMAT_STR), datetime.now().year)
    return render(request, 'index.html', dictionary={'weekstr': weekstr, 'form': form})

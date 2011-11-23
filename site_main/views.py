# Create your views here.
from models import *
from django.shortcuts import *
from forms import *

def home(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
    else:
        form = ClientForm()
    return render(request, 'index.html', dictionary={'form': form})

from models import *
from django.db.models import Q

class Matcher:
    def __init__(self, myclient):
        self.client = myclient # myself
        self.match = None # the match, if there is one
        self.__findMatch()

    def __findMatch(self): # overlapping m2m fields FTW!
        days = self.client.day_prefs.values_list('pk', flat=True)
        rests = self.client.restaurant_prefs.values_list('pk', flat=True)

        s = Client.objects.filter(day_prefs__pk__in=days, restaurant_prefs__pk__in=rests).exclude(person=self.client).order_by('?')
        if s.exists():
            self.match = s[0]

    def __nonzero__(self):
        return self.match != None

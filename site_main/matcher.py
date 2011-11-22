from models import *
from random import choice

class Matcher:
    def __init__(self, myclient):
        self.client = myclient # myself
        self.match = None # the match, if there is one
        self.__findMatch()

    def __findMatch(self): # overlapping m2m fields FTW!
        days = self.client.day_prefs.values_list('pk', flat=True)
        rests = self.client.restaurant_prefs.values_list('pk', flat=True)

        s = Client.objects.filter(day_prefs__pk__in=days, restaurant_prefs__pk__in=rests).exclude(person=self.client).distinct().order_by('?')
        if s.exists():
            self.match = s[0]

    def suggest_day(self): # randomly suggest a day that works for both the client and the match
        if self.match:
            days = set(self.client.day_prefs.all()) & set(self.match.day_prefs.all())
            return choice(tuple(days))
        return None

    def suggest_restaurant(self): # randomly suggest a restaurant that works for both the client and the match
        if self.match:
            cats = set(self.client.restaurant_prefs.all()) & set(self.match.restaurant_prefs.all())
            rcat = choice(tuple(cats))
            return Restaurant.objects.filter(category=rcat).order_by('?')[0]
        return None

    def __nonzero__(self):
        return self.match != None

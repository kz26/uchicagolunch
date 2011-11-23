from models import *
from random import choice
from datehelper import *

class Matcher:
    def __init__(self, myclient):
        self.client = myclient # myself
        self.match = None # the match, if there is one
        self.__matchobj = None
        self.__findMatch()

    def __findMatch(self): # overlapping m2m fields FTW!
        days = self.client.day_prefs.values_list('pk', flat=True)
        rests = self.client.restaurant_prefs.values_list('pk', flat=True)

        s = Client.objects.exclude(person=self.client).filter(day_prefs__pk__in=days, restaurant_prefs__pk__in=rests, matched=False).distinct()
        if s.exists():
            self.match = s[0]

    def __suggest_day(self): # randomly suggest a day that works for both the client and the match
        if self.match:
            days = set(self.client.day_prefs.all()) & set(self.match.day_prefs.all())
            return choice(tuple(days)).num # returns the number, not the actual Day object
        return None

    def suggest_restaurant(self): # randomly suggest a restaurant that works for both the client and the match
        if self.match:
            cats = set(self.client.restaurant_prefs.all()) & set(self.match.restaurant_prefs.all())
            rcat = choice(tuple(cats))
            return Restaurant.objects.filter(category=rcat).order_by('?')[0]
        return None

    def suggest_datetime(self): # returns a datetime object representing the match date/time
        if self.match:
            d = getDateOffset(getNextWeekNow()[0], self.__suggest_day())
            t = time(12)
            offset = timedelta(minutes=choice(range(0, 135, 15))) # and increase in random 15-min intervals until 2pm
            return datetime.combine(d, t) + offset
        return None

    def get_match(self): # sets matched to True in both self and match, and creates a match object
        if self.__matchobj:
            return self.__matchobj
        elif self.match:
            self.client.matched = True
            self.match.matched = True
            self.client.save()
            self.match.save()
            m = Match.objects.create(person1=self.client.person, person2=self.match.person, location=self.suggest_restaurant(), date=self.suggest_datetime()) 
            self.__matchobj = m
            return m
        return None

    def __nonzero__(self):
        return self.match != None

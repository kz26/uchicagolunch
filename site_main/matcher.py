from models import *
from random import choice
from datehelper import *
import sys

class Matcher:
    def __init__(self, myclient):
        self.client = myclient # myself
        self.match = None # the match, if there is one
        self.__matchobj = None
        self.__findMatch()

    def __findMatch(self): # overlapping m2m fields FTW!
        days = self.client.day_prefs.values_list('pk', flat=True)
        rests = self.client.restaurant_prefs.values_list('pk', flat=True)

        s = Client.objects.filter(day_prefs__pk__in=days, restaurant_prefs__pk__in=rests, matched=False).exclude(person=self.client.person).distinct()
        if s.exists():
            #s = [client for client in s if client.matched == False]
            self.match = choice(s)
            #sys.stdout.write("Matched %s with %s\n" % (self.client.person.name, self.match.person.name))

    def __suggest_day(self): # randomly suggest a day that works for both the client and the match
        if self.match:
            days = set(self.client.day_prefs.all()) & set(self.match.day_prefs.all())
            return choice(tuple(days)) # returns the number, not the actual Day object
        return None

    def suggest_restaurant(self): # randomly suggest a restaurant that works for both the client and the match
        if self.match:
            cats = set(self.client.restaurant_prefs.all()) & set(self.match.restaurant_prefs.all())
            catlist = [c.pk for c in tuple(cats)]
            rlist = Restaurant.objects.filter(category__pk__in=catlist)
            return choice(tuple(rlist))
        return None

    def suggest_datetime(self): # returns a datetime object representing the match date/time
        if self.match:
            d = self.__suggest_day().date
            t = time(12)
            offset = timedelta(minutes=choice(range(0, 135, 15))) # and increase in random 15-min intervals until 2pm
            return datetime.combine(d, t) + offset
        return None

    def get_match(self): # sets matched to True in both self and match, and creates a match object
        if self.__matchobj is not None:
            return self.__matchobj
        elif self.match:
            self.client.matched = True
            self.match.matched = True
            self.client.save()
            self.match.save()
            #sys.stdout.write("%s: matched = %s\n" % (self.client.person.name, self.client.matched))
            #sys.stdout.write("%s: matched = %s\n" % (self.match.person.name, self.client.matched))
            m = Match(person1=self.client.person, person2=self.match.person, location=self.suggest_restaurant(), date=self.suggest_datetime()) 
            m.save()
            #sys.stdout.write("Created match object with %s and %s\n" % (self.client.person.name, self.match.person.name))
            self.__matchobj = m
            return m
        return None

    def __nonzero__(self):
        #if self.match:
            #sys.stdout.write("%s has a match\n" % (self.client.person.name))
        return self.match != None

from django.db import models
from datehelper import *

# Create your models here.

class RestaurantCategory(models.Model):
    value = models.CharField(max_length=100)
    def __unicode__(self):
        return self.value

class Restaurant(models.Model):
    category = models.ForeignKey(RestaurantCategory)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class Day(models.Model):
    num = models.IntegerField(primary_key=True) # 0 = Sunday, 6 = Saturday
    #name = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return getDateOffset(getNextWeekNow()[0], self.num).strftime("%A, %b %d")

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    def __unicode__(self):
        return self.name

class Client(models.Model):
    person = models.ForeignKey(Person)
    restaurant_prefs = models.ManyToManyField(RestaurantCategory, verbose_name='What kind of food do you like?')
    day_prefs = models.ManyToManyField(Day, verbose_name='What\'s your availability?')
    created = models.DateTimeField(auto_now_add=True)
    matched = models.BooleanField()

class Match(models.Model):
    person1 = models.ForeignKey(Person, related_name='person1')
    person2 = models.ForeignKey(Person, related_name='person2')
    location = models.ForeignKey(Restaurant)
    date = models.DateTimeField()

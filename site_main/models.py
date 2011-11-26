from django.db import models
from datehelper import *
from django.conf import settings

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
    day_prefs = models.ManyToManyField(Day, verbose_name='When are you available for lunch?')
    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField()
    matched = models.BooleanField()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.expires = datetime.now() + timedelta(days=settings.EXPIRY_DAYS)
        super(Client, self).save(*args, **kwargs)

class Match(models.Model):
    person1 = models.ForeignKey(Person, related_name='person1')
    person2 = models.ForeignKey(Person, related_name='person2')
    location = models.ForeignKey(Restaurant)
    date = models.DateTimeField()

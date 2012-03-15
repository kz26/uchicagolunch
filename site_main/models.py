from django.db import models
from django.conf import settings
from datetime import date, timedelta, datetime
from acgen import *

# Create your models here.

class RestaurantCategory(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Restaurant categories'

    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Restaurant(models.Model):
    class Meta:
        ordering = ['name']
    category = models.ForeignKey(RestaurantCategory)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    def __unicode__(self):
        return self.name

class Request(models.Model):
    class Meta:
        ordering = ['-created']

    created = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField()
    expire_notified = models.BooleanField()
    matched = models.BooleanField()
    name = models.CharField(max_length=100, verbose_name='Name (first and last)')
    email = models.EmailField()
    restaurant_prefs = models.ManyToManyField(RestaurantCategory, verbose_name='What kind of food do you like?')
    active = models.BooleanField()
    activation_key = models.CharField(max_length=128, editable=False)

    def __unicode__(self):
        return "%s <%s>" % (self.name, self.email)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.activation_key = GenRandomKey(64)
        super(Request, self).save(*args, **kwargs)

class Day(models.Model):
    class Meta:
        ordering = ['-date']
    request = models.ForeignKey(Request)
    date = models.DateField()

    def __unicode__(self):
        return "%s - %s" % (self.request.name, self.date.strftime("%A, %b. %d, %Y"))

class Match(models.Model):
    class Meta:
        verbose_name_plural = 'Matches'

    request1 = models.ForeignKey(Request, related_name='request1')
    request2 = models.ForeignKey(Request, related_name='request2')
    location = models.ForeignKey(Restaurant)
    date = models.DateTimeField()
    def __unicode__(self):
        return "(%s, %s)" % (self.request1.name, self.request2.name)

class Ban(models.Model):
    email = models.EmailField()

class IPBan(models.Model):
    ip = models.IPAddressField()
    def __unicode__(self):
        return str(self.ip)

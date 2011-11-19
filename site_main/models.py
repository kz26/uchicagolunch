from django.db import models

# Create your models here.

class RestaurantCategory(models.Model):
    value = models.CharField(max_length=100)

class Restaurant(models.Model):
    category = models.ForeignKey(RestaurantCategory)
    name = models.CharField(max_length=100)

class Day(models.Model):
    name = models.CharField(max_length=100)

class Client(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    restaurant_prefs = models.ManyToManyField(RestaurantCategory)
    day_prefs = models.ManyToManyField(Day)
    created = models.DateTimeField(auto_now_add=True)

class Match(models.Model):
    client1 = models.ForeignKey(Client) 
    client2 = models.ForeignKey(Client) 
    location = models.ForeignKey(Restaurant)
    date = models.DateTimeField()


from django.db import models

# Create your models here.
from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=200)
    def __str__(self):
        return self.city_name

class BusinessEvent(models.Model):
    recordedTime = models.DateTimeField('recorded time')
    to_city = models.ForeignKey(City)

    def asXML():
      return "foo"

class MailDelivery(models.Model):
    weight = models.IntegerField()
    volume = models.IntegerField()
    priority = models.CharField(max_length=200)
    day = models.CharField(max_length=200)

class TransportCostUpdate(models.Model):
    company = models.CharField(max_length=200)
    transport_type = models.CharField(max_length=200)
    weight_cost = models.IntegerField()
    volume_cost = models.IntegerField()
    max_weight = models.IntegerField()
    max_volume = models.IntegerField()
    duration = models.IntegerField()
    frequency = models.IntegerField()
    day = models.CharField(max_length=200)
    is_active = models.BooleanField()

class PriceUpdate():
    priority = models.CharField(max_length=200)
    weight_cost = models.IntegerField()
    volume_cost = models.IntegerField()

class TransportDiscontinued():
    company = models.CharField(max_length=200)
    transport_discontinued_type = models.CharField(max_length=200)





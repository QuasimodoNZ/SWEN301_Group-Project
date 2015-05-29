# Create your models here.
from django.db import models

PRIORITIES = (
    ('Land', 'Land'),
    ('Sea', 'Sea'),
    ('Air', 'Air'),
)
DAYS = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
)

class City(models.Model):
    city_name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural='Cities'

    def __str__(self):
        return self.city_name

class Company(models.Model):
    company_name = models.CharField(max_length=200)
    
    class Meta:
        verbose_name_plural='Companies'
    
    def __str__(self):
        return self.company_name

class BusinessEvent(models.Model):
    recorded_time = models.DateTimeField('recorded time', auto_now_add=True)
    to_city = models.ForeignKey(City, related_name='%(app_label)s_%(class)s_destination')
    from_city = models.ForeignKey(City, related_name='%(app_label)s_%(class)s_source')
    priority = models.CharField(choices=PRIORITIES, max_length=4)

    def __str__(self):
        return '{}-{}:{}'.format(self.from_city, self.to_city, self.priority)

    def asXML(self):
        return "foo"
    
    class Meta:
        abstract = True

class MailDelivery(BusinessEvent):
    weight = models.IntegerField('weight in grams')
    volume = models.IntegerField('volume in cubic centimeter')
    
    class Meta:
        verbose_name_plural='Mail Deliveries'

class TransportCostUpdate(BusinessEvent):
    company = models.ForeignKey(Company)
    weight_cost = models.IntegerField('cost per gram')
    volume_cost = models.IntegerField('cost per cubic centimeter')
    max_weight = models.IntegerField('maximum weight in grams')
    max_volume = models.IntegerField('maximum volume in cubic centimeters')
    duration = models.IntegerField('duration of trip in hours')
    frequency = models.IntegerField('number of hours between each departure')
    day = models.CharField('day of the week the transport departs', choices=DAYS, max_length=8)
    is_active = models.BooleanField('if the model is currently active')
    
    def get_opposite(self, city):
        if city == self.from_city:
            return self.to_city
        elif city == self.to_city:
            return self.from_city
        else:
            return None

class PriceUpdate(BusinessEvent):
    weight_cost = models.IntegerField('cost per gram')
    volume_cost = models.IntegerField('cost per cubic centimeter')

class TransportDiscontinued(BusinessEvent):
    company = models.ForeignKey(Company)





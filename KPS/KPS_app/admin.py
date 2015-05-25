from django.contrib import admin

from KPS_app.models import City, Company, BusinessEvent, MailDelivery, TransportCostUpdate, PriceUpdate,TransportDiscontinued
# Register your models here.
admin.site.register(City)
admin.site.register(Company)
admin.site.register(MailDelivery)
admin.site.register(TransportCostUpdate)
admin.site.register(PriceUpdate)
admin.site.register(TransportDiscontinued)
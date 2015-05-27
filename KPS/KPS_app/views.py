from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from KPS_app import models

# Create your views here.
class Dashboard(TemplateView):
    template_name = "KPS_app/dashboard.html"
    model = models.BusinessEvent
    rev_total = 200000

class DeliverMail(CreateView):
    template_name = 'KPS_app/deliver_mail.html'
    model = models.MailDelivery
    fields = ['from_city', 'to_city', 'priority', 'weight', 'volume']
    
class CustomerUpdate(CreateView):
    template_name = 'KPS_app/customer_update.html'
    model = models.PriceUpdate
    fields = ['from_city', 'to_city', 'priority', 'weight_cost', 'volume_cost']
    
class TransportUpdate(CreateView):
    template_name = 'KPS_app/transport_update.html'
    model = models.TransportCostUpdate
    fields = ['from_city', 'to_city', 'priority', 'company', 'weight_cost', 'volume_cost', 'max_weight', 'max_volume', 'duration', 'frequency', 'day', 'is_active']

class TransportDiscontinued(CreateView):
    template_name = 'KPS_app/transport_discontinue.html'
    model = models.TransportDiscontinued
    fields = ['from_city', 'to_city', 'priority', 'company']

from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from KPS_app import models
from datetime import datetime
from KPS_app.forms import CityForm, CompanyForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.
class Dashboard(TemplateView):
    template_name = "KPS_app/dashboard.html"
    def get_context_data(self, **kwargs):
        rtn = TemplateView.get_context_data(self, **kwargs)
        rtn['event_total'] = get_event_log()
        rtn['table1'] = [("Wellington",   "Wellington", "Land", "456", "127"),
                         ("Wellington",   "Auckland",   "Air",  "789", "180"),
                         ("Christchurch", "Auckland",   "Sea",  "3432", "1258"),
                         ("Wellington",   "Auckland",   "Land", "2432",  "565")]
        return rtn

class DeliverMail(CreateView):
    success_url = '/'
    template_name = 'KPS_app/deliver_mail.html'
    model = models.MailDelivery
    fields = ['from_city', 'to_city', 'priority', 'weight', 'volume']

class CustomerUpdate(CreateView):
    success_url = '/'
    template_name = 'KPS_app/customer_update.html'
    model = models.PriceUpdate
    fields = ['from_city', 'to_city', 'priority', 'weight_cost', 'volume_cost']

class TransportUpdate(CreateView):
    success_url = '/'
    template_name = 'KPS_app/transport_update.html'
    model = models.TransportCostUpdate
    fields = ['from_city', 'to_city', 'priority', 'company', 'weight_cost', 'volume_cost', 'max_weight', 'max_volume', 'duration', 'frequency', 'day', 'is_active']

class TransportDiscontinued(CreateView):
    success_url = '/'
    template_name = 'KPS_app/transport_discontinue.html'
    model = models.TransportDiscontinued
    fields = ['from_city', 'to_city', 'priority', 'company']

def add_cities_and_companies(request):
    if request.method == "POST":
        print(request.POST)
        city_form = CityForm(request.POST, instance=models.City())
        company_form = CompanyForm(request.POST, instance=models.Company())
        if city_form.is_valid() and company_form.is_valid():
            if not request.POST['city_name'] == '' and len(models.City.objects.filter(city_name=request.POST['city_name'])) == 0:
                city_form.save()
            if not request.POST['city_name'] == '' and len(models.City.objects.filter(city_name=request.POST['city_name'])) == 0:
                company_form.save()
            return HttpResponseRedirect('/')
    else:
        city_form = CityForm(instance=models.City())
        company_form = CompanyForm(instance=models.Company())
    return render_to_response('KPS_app/cities_and_companies.html', {'city_form':city_form, 'company_form':company_form},  RequestContext(request))

def get_network(time=None):
    events = get_event_log(time)

def get_event_log(time=None):
    if time == None:
        time = datetime.now()

    deliveries = models.MailDelivery.objects.filter(recorded_time__lte=time).count()
    prices = models.PriceUpdate.objects.filter(recorded_time__lte=time).count()
    costs = models.TransportCostUpdate.objects.filter(recorded_time__lte=time).count()
    discontinues = models.TransportDiscontinued.objects.filter(recorded_time__lte=time).count()

    events = deliveries + prices + costs + discontinues



    return events

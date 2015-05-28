from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from KPS_app import models
from datetime import datetime
from KPS_app.forms import CityForm, CompanyForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from collections import deque

# Create your views here.
class Dashboard(TemplateView):
    template_name = "KPS_app/dashboard.html"
    
    def get_context_data(self, **kwargs):
        rtn = TemplateView.get_context_data(self, **kwargs)
        
        rtn['events'] = get_event_log()
        
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
    return render_to_response('KPS_app/cities_and_companies.html', {'city_form':city_form, 'company_form':company_form}, RequestContext(request))

class Network():
    def __init__(self, time=None):
        
        self.nodes = {} # {models.City -> [models.TransportCostUpdate]
        self.links = {} # {(from, to, company, type) -> models.TransportCostUpdate}

        self.update(get_event_log(time))
        
    def update(self, events):
        for event in events:
            t = as_tuple(event)
            if type(event) == models.TransportCostUpdate:
                if t in self.links: # we are updating a transport cost must update the node list
                    node_links = self.nodes[event.from_city]
                    for i, tcu in enumerate(node_links):
                        if as_tuple(tcu) == t:
                            node_links[i] = event    
                    node_links = self.nodes[event.to_city]
                    for i, tcu in enumerate(node_links):
                        if as_tuple(tcu) == t:
                            node_links[i] = event
                            
                else:
                    self.links[event.from_city].append(event)
                    self.links[event.to_city].append(event)
                self.links[t] = event

            elif type(event) == models.TransportDiscontinued: # got to remove it from the network
                self.links.pop(as_tuple(event), None)
                self.nodes[event.to_city].remove(event)
                self.nodes[event.from_city].remove(event)
                
            else:
                print('I don\'t know what this model is: {}'.format(event))
        
    def find_path(self, source, destination, priority):
        '''Return list of TransportUpdateCost'''
        
        for city, links in self.nodes.iteritems():
            links.sortt(key=lambda x: x.volume_cost*x.weight_cost)
        
        visited = []
        q = deque([source])
        while len(q) >0:
            n = q.popleft()
            
            
        
        pass
                                
def as_tuple(event):
    return (event.from_city, event.to_city, event.company, event.priority)
        
def get_event_log(time=None):
    if time == None:
        time = datetime.now()
    
    deliveries = models.MailDelivery.objects.filter(recorded_time__lte=time)
    prices = models.PriceUpdate.objects.filter(recorded_time__lte=time)
    costs = models.TransportCostUpdate.objects.filter(recorded_time__lte=time)
    discontinues = models.TransportDiscontinued.objects.filter(recorded_time__lte=time)
    
    events = sorted(list(deliveries) + list(prices) + list(costs) + list(discontinues), key=lambda event: event.recorded_time, reverse=True)
        
    return events

def get_revenue_cost(delivery):
    prices = models.PriceUpdate.objects.filter(recorded_time__lte=delivery.recorded_time).order_by('recorded_time').reverse()
    # find the revenue
    for price in prices:
        if (delivery.from_city, delivery.to_city, delivery.priority) == (price.from_city, price.to_city, price.priority):
            return delivery.weight * price.weight_cost + delivery.volume * price.volume_cost
    
    ###### find the cost
    # find path at that time
    path = Network(delivery.recorded_time).find_path(delivery.from_city, delivery.to_city, delivery.priority)
    
    # move across path calculating cost
    expenditure = sum(delivery.weight * p.weight_cost + delivery.volume * p.volume_cost for p in  path)
    

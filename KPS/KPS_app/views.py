from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView
from KPS_app import models
from datetime import datetime
from KPS_app.forms import CityForm, CompanyForm, MailDeliveryForm,\
    TransportDiscontinueForm
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from django.http import HttpResponse

# Create your views here.
class Dashboard(TemplateView):
    template_name = "KPS_app/dashboard.html"

    def get_context_data(self, **kwargs):
        rtn = TemplateView.get_context_data(self, **kwargs)
        rtn['revenue'] = 21564
        rtn['expenditure'] =  654
        rtn['event_total'] = len(get_event_log())
        rtn['table1'] = [("Wellington",   "Wellington", "Land", "456", "127"),
                         ("Wellington",   "Auckland",   "Air",  "789", "180"),
                         ("Christchurch", "Auckland",   "Sea",  "3432", "1258"),
                         ("Wellington",   "Auckland",   "Land", "2432",  "565")]
        return rtn


class DeliverMail(FormView):
    success_url = '/'
    template_name = 'KPS_app/deliver_mail.html'
    form_class = MailDeliveryForm

    def form_valid(self, form):
        price_update_selection = self.request.POST['price_update']
        price_update_selection = models.PriceUpdate.objects.get(pk=price_update_selection)
        mail = models.MailDelivery(weight = self.request.POST['weight'],
            volume = self.request.POST['volume'],
            to_city = price_update_selection.to_city,
            from_city = price_update_selection.from_city,
            priority = price_update_selection.priority)
        mail.save()
        return HttpResponseRedirect(self.success_url)

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

class TransportDiscontinued(FormView):
    success_url = '/'
    template_name = 'KPS_app/transport_discontinue.html'
    form_class = TransportDiscontinueForm

    def get_form(self, form_class=None):
        
        return TransportDiscontinueForm(((link.pk, '{} {}'.format(link.company, str(link))) for link in Network().links.values()))
        

    def form_valid(self, form):
        transport_update = self.request.POST['transport_update']
        transport_update = models.TransportCostUpdate.objects.get(pk=transport_update)
        discontinue = models.TransportDiscontinued(
            from_city=transport_update.from_city,
            to_city=transport_update.to_city,
            priority=transport_update.priority,
            company=transport_update.company
        )
        discontinue.save()
        return HttpResponseRedirect(self.success_url)

def add_cities_and_companies(request):
    if request.method == "POST":
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
            if type(event) == models.TransportCostUpdate:
                t = as_tuple(event)
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
                    if event.from_city not in self.nodes:
                        self.nodes[event.from_city] = []
                    self.nodes[event.from_city].append(event)
                    if event.to_city not in self.nodes:
                        self.nodes[event.to_city] = []
                    self.nodes[event.to_city].append(event)
                self.links[t] = event

            elif type(event) == models.TransportDiscontinued: # got to remove it from the network
                self.links.pop(as_tuple(event), None)
                self.nodes[event.to_city].remove(event)
                self.nodes[event.from_city].remove(event)

            else:
                print('I don\'t know what this model is: {}'.format(event))

    def find_path(self, source, destination, priority):
        '''Return list of TransportUpdateCost'''

        for links in self.nodes.itervalues():
            links.sort(key=lambda x: x.volume_cost*x.weight_cost)

        visited = []
        queue = [(0, source, None, None)] # [(priority or cost int, node City, from tuple, using TransportRoute), ...]
        while len(queue) > 0:
            t = queue.pop(0)
            if t[1] == destination:
                path = []
                while t[2] != None:
                    path.append(t[3])
                    t = t[2]
                return list(reversed(path))
            elif t[1] in visited:
                continue
            visited.append(t)
            if t[1] not in self.nodes: # actually only happens at the very start
                continue
            for link in self.nodes[t[1]]:
                queue.append((t[0] + link.volume_cost*link.weight_cost, link.get_opposite(t[1]), t, link))
            queue.sort()

        # Mustn't have found a path
        return None

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


def get_xml(request):
    xml = ("<events>" +
        serializers.serialize('xml', models.MailDelivery.objects.all()) +
        serializers.serialize('xml', models.TransportCostUpdate.objects.all()) +
        serializers.serialize('xml', models.PriceUpdate.objects.all()) +
        serializers.serialize('xml', models.TransportDiscontinued.objects.all()) +
        "</events>"
    )
    return HttpResponse(xml)

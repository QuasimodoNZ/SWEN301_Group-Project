from django.conf.urls import patterns, url

from KPS_app import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^$', views.Dashboard.as_view(), name='home'),
    url(r'^deliver-mail/$', login_required(views.DeliverMail.as_view()), name='deliver_mail'),
    url(r'^update-price/$', login_required(views.CustomerUpdate.as_view()), name='update_price'),
    url(r'^update-cost/$', login_required(views.TransportUpdate.as_view()), name='update_cost'),
    url(r'^discontinue-transport/$', login_required(views.TransportDiscontinued.as_view()), name='discontinue_transport'),
    
)

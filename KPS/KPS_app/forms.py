'''
Created on 25/05/2015

@author: Benjamin Riddell
'''
from django import forms
from KPS_app import models
from datetime import datetime
from django.forms.fields import ChoiceField

class CityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CityForm, self).__init__(*args, **kwargs)

        self.fields['city_name'].required = False

    class Meta:
        model = models.City
        fields = ['city_name']

class CompanyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        self.fields['company_name'].required = False

    class Meta:
        model = models.Company
        fields = ['company_name']

class MailDeliveryForm(forms.ModelForm):
    price_update = forms.ModelChoiceField(queryset=models.PriceUpdate.objects.all())

    class Meta:
        model = models.MailDelivery
        fields = ['weight', 'volume']

class TransportDiscontinueForm(forms.ModelForm):
    transport_update = ChoiceField(choices=(-1,'Error: No choices available'), required=True)

    def __init__(self, link_choices, *args, **kwargs):
        super(TransportDiscontinueForm, self).__init__(*args, **kwargs)
        if link_choices:
            self.fields['transport_update'].choices = link_choices

    class Meta:
        model = models.TransportDiscontinued
        fields = []



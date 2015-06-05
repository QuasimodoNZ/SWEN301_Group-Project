'''
Created on 25/05/2015

@author: Benjamin Riddell
'''
from django import forms
from KPS_app import models

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

def get_price_choices():
    return ((pu.pk, str(pu)) for pu in models.PriceUpdate.objects.all())

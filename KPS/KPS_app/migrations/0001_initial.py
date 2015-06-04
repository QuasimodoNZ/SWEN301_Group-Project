# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city_name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='MailDelivery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recorded_time', models.DateTimeField(auto_now_add=True, verbose_name=b'recorded time')),
                ('priority', models.CharField(max_length=4, choices=[(b'Land', b'Land'), (b'Sea', b'Sea'), (b'Air', b'Air')])),
                ('weight', models.IntegerField(verbose_name=b'weight in grams')),
                ('volume', models.IntegerField(verbose_name=b'volume in cubic centimeter')),
                ('from_city', models.ForeignKey(related_name='kps_app_maildelivery_source', to='KPS_app.City')),
                ('to_city', models.ForeignKey(related_name='kps_app_maildelivery_destination', to='KPS_app.City')),
            ],
            options={
                'verbose_name_plural': 'Mail Deliveries',
            },
        ),
        migrations.CreateModel(
            name='PriceUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recorded_time', models.DateTimeField(auto_now_add=True, verbose_name=b'recorded time')),
                ('priority', models.CharField(max_length=4, choices=[(b'Land', b'Land'), (b'Sea', b'Sea'), (b'Air', b'Air')])),
                ('weight_cost', models.IntegerField(verbose_name=b'cost per gram')),
                ('volume_cost', models.IntegerField(verbose_name=b'cost per cubic centimeter')),
                ('from_city', models.ForeignKey(related_name='kps_app_priceupdate_source', to='KPS_app.City')),
                ('to_city', models.ForeignKey(related_name='kps_app_priceupdate_destination', to='KPS_app.City')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransportCostUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recorded_time', models.DateTimeField(auto_now_add=True, verbose_name=b'recorded time')),
                ('priority', models.CharField(max_length=4, choices=[(b'Land', b'Land'), (b'Sea', b'Sea'), (b'Air', b'Air')])),
                ('weight_cost', models.IntegerField(verbose_name=b'cost per gram')),
                ('volume_cost', models.IntegerField(verbose_name=b'cost per cubic centimeter')),
                ('max_weight', models.IntegerField(verbose_name=b'maximum weight in grams')),
                ('max_volume', models.IntegerField(verbose_name=b'maximum volume in cubic centimeters')),
                ('duration', models.IntegerField(verbose_name=b'duration of trip in hours')),
                ('frequency', models.IntegerField(verbose_name=b'number of hours between each departure')),
                ('day', models.CharField(max_length=8, verbose_name=b'day of the week the transport departs', choices=[(b'Monday', b'Monday'), (b'Tuesday', b'Tuesday'), (b'Wednesday', b'Wednesday'), (b'Thursday', b'Thursday'), (b'Friday', b'Friday'), (b'Saturday', b'Saturday'), (b'Sunday', b'Sunday')])),
                ('is_active', models.BooleanField(verbose_name=b'if the model is currently active')),
                ('company', models.ForeignKey(to='KPS_app.Company')),
                ('from_city', models.ForeignKey(related_name='kps_app_transportcostupdate_source', to='KPS_app.City')),
                ('to_city', models.ForeignKey(related_name='kps_app_transportcostupdate_destination', to='KPS_app.City')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransportDiscontinued',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recorded_time', models.DateTimeField(auto_now_add=True, verbose_name=b'recorded time')),
                ('priority', models.CharField(max_length=4, choices=[(b'Land', b'Land'), (b'Sea', b'Sea'), (b'Air', b'Air')])),
                ('company', models.ForeignKey(to='KPS_app.Company')),
                ('from_city', models.ForeignKey(related_name='kps_app_transportdiscontinued_source', to='KPS_app.City')),
                ('to_city', models.ForeignKey(related_name='kps_app_transportdiscontinued_destination', to='KPS_app.City')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

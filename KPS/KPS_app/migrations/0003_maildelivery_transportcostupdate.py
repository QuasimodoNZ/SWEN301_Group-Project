# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KPS_app', '0002_businessevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailDelivery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.IntegerField()),
                ('volume', models.IntegerField()),
                ('priority', models.CharField(max_length=200)),
                ('day', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TransportCostUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.CharField(max_length=200)),
                ('transport_type', models.CharField(max_length=200)),
                ('weight_cost', models.IntegerField()),
                ('volume_cost', models.IntegerField()),
                ('max_weight', models.IntegerField()),
                ('max_volume', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('frequency', models.IntegerField()),
                ('day', models.CharField(max_length=200)),
                ('is_active', models.BooleanField()),
            ],
        ),
    ]

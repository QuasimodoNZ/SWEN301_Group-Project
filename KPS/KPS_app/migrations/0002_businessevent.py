# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KPS_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recordedTime', models.DateTimeField(verbose_name=b'recorded time')),
                ('to_city', models.ForeignKey(to='KPS_app.City')),
            ],
        ),
    ]

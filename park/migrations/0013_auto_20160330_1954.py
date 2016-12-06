# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-30 19:54
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('park', '0012_spot_sv_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='sv_location',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
    ]

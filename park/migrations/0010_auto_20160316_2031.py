# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-16 20:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('park', '0009_auto_20160311_0943'),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('phone_number', models.CharField(max_length=20)),
                ('rating', models.IntegerField(default=0)),
                ('num_ratings', models.IntegerField(default=0)),
                ('num_reservations', models.IntegerField(default=0)),
                ('stripe_id', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='geobucket',
            name='price',
            field=models.IntegerField(default=500),
        ),
        migrations.AddField(
            model_name='geobucket',
            name='reservations',
            field=models.IntegerField(default=0),
        ),
    ]
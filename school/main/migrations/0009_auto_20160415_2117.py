# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-15 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20160415_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='menu',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shinyapp',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
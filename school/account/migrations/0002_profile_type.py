# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-07 03:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='type',
            field=models.IntegerField(default=0),
        ),
    ]

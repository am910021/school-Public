# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-30 14:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0011_auto_20160530_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='type',
            field=models.CharField(default=datetime.datetime(2016, 5, 30, 14, 16, 13, 563738, tzinfo=utc), max_length=32),
            preserve_default=False,
        ),
    ]

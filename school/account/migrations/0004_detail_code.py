# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-14 03:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20160314_0335'),
    ]

    operations = [
        migrations.AddField(
            model_name='detail',
            name='code',
            field=models.CharField(blank=True, max_length=32),
        ),
    ]
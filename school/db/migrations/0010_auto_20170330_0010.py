# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-03-29 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0009_case_funds_dpment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case_funds',
            name='cas_funds',
            field=models.IntegerField(),
        ),
    ]

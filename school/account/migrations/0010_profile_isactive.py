# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-03 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_remove_profile_groupqty'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
    ]
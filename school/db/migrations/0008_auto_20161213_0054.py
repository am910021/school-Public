# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-12 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0007_auto_20161208_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studsem_all',
            name='dep_fname',
            field=models.CharField(max_length=32),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-31 05:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0012_salary_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salary',
            old_name='type',
            new_name='title',
        ),
    ]

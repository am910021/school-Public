# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-12-03 08:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_auto_20161203_1554'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Dep2',
            new_name='Dep',
        ),
    ]

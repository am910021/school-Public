# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-03-29 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0008_auto_20161213_0054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Case_funds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cas_key', models.CharField(max_length=20)),
                ('cas_funds', models.IntegerField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Dpment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acy', models.IntegerField()),
                ('dep_no', models.CharField(max_length=20)),
                ('dep_fname', models.CharField(max_length=128)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-30 16:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0008_auto_20160420_2314'),
    ]

    operations = [
        migrations.CreateModel(
            name='Studsem_all',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sts_acy', models.IntegerField()),
                ('sts_sem', models.IntegerField()),
                ('std_serno', models.CharField(max_length=64)),
                ('cls_id', models.CharField(max_length=16)),
                ('cls_name', models.CharField(max_length=32)),
                ('sec_name', models.CharField(max_length=16)),
                ('sub_name', models.CharField(max_length=32)),
                ('sub_name2', models.CharField(max_length=32)),
                ('col_fname', models.CharField(max_length=32)),
                ('dep_no', models.CharField(max_length=16)),
                ('dep_fname', models.CharField(max_length=32)),
                ('cls_year', models.IntegerField()),
                ('cls_class', models.CharField(max_length=1)),
                ('sts_status', models.IntegerField()),
                ('msg_name', models.CharField(max_length=64)),
                ('sts_ptpone', models.CharField(max_length=1)),
                ('sts_back', models.CharField(max_length=1)),
                ('sts_tsch', models.CharField(max_length=1)),
                ('sts_tdep', models.CharField(max_length=1)),
                ('sts_five', models.CharField(max_length=1)),
                ('std_sex', models.CharField(max_length=1)),
                ('esc_code', models.CharField(max_length=16)),
                ('esc_name', models.CharField(max_length=32)),
                ('eqa_code', models.CharField(max_length=16)),
                ('eqa_name', models.CharField(max_length=32)),
                ('eid_code', models.CharField(max_length=16)),
                ('eid_name', models.CharField(max_length=32)),
                ('eid_code_a', models.CharField(max_length=16)),
                ('eid_name2', models.CharField(max_length=32)),
                ('sch_code', models.CharField(max_length=16)),
                ('sch_fname', models.CharField(max_length=32)),
                ('sdp_code', models.CharField(max_length=64)),
                ('sdp_name', models.CharField(max_length=64)),
                ('prv_code_n', models.CharField(max_length=64)),
                ('prv_name', models.CharField(max_length=64)),
                ('abg_code', models.CharField(max_length=64)),
                ('abg_name', models.CharField(max_length=64)),
                ('zip_name1', models.CharField(max_length=64)),
                ('zip_name2', models.CharField(max_length=64)),
                ('std_entym', models.CharField(max_length=16)),
                ('hst_type', models.CharField(max_length=16)),
                ('hst_acy', models.CharField(max_length=16)),
                ('hst_sem', models.CharField(max_length=16)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 00:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20171005_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='quickview',
            name='Status',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

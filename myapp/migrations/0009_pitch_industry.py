# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-05 07:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_portfolio'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitch',
            name='industry',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
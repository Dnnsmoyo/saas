# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-05 16:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20181205_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
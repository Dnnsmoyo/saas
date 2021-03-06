# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-12-04 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20181201_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('cell', models.IntegerField()),
                ('next_of_kin', models.CharField(max_length=100)),
                ('next_of_kin_cell', models.IntegerField()),
                ('website', models.URLField()),
                ('investment_interest', models.DecimalField(decimal_places=2, max_digits=100)),
                ('investments', models.TextField()),
                ('annual_investment_budget', models.DecimalField(decimal_places=2, max_digits=100)),
                ('investment_portfolio', models.FileField(upload_to='media')),
                ('offshore_investments', models.TextField()),
                ('banking_details', models.TextField()),
                ('risk_level', models.CharField(choices=[('Very High', 'Very High'), ('High', 'High'), ('Medium', 'Medium')], max_length=100)),
            ],
        ),
    ]

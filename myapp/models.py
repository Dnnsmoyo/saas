# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

Category = (
	('Student',('Student')),
	('Entreprener',('Entreprener')),
	('Expat',('Expat/Diasporan')),
	('Trust',('Trust')),
	('Institutional',('Institutional')),
	('Civil Servant',('Civil Servant')),
	('Other',('Other')),

	)
Marital_Status = (
	('Single',('Single')),
	('Married',('Married')),
	('Divorced',('Divorced')),

	)

class Personal(models.Model):
	user = models.OneToOneField(get_user_model())
	address = models.TextField()
	category = models.CharField(choices=Category,max_length=100)
	cell = models.IntegerField()
	next_of_kin = models.CharField(max_length=100)
	maritality = models.CharField(max_length=100,choices=Marital_Status)
	banking_details = models.TextField()

class Company(models.Model):
	user = models.OneToOneField(get_user_model())
	name = models.CharField(max_length=100)
	address = models.IntegerField()
	website = models.URLField(max_length=100)
	email = models.EmailField(max_length=100)
	contact = models.TextField()


class Daily(models.Model):
	user = models.OneToOneField(get_user_model())
	email = models.EmailField(max_length=100)
	date_created = models.DateTimeField(auto_now=True)

class Weekly(models.Model):
	user = models.OneToOneField(get_user_model())
	email = models.EmailField(max_length=100)
	date_created = models.DateTimeField(auto_now=True)

class Monthly(models.Model):
	user = models.OneToOneField(get_user_model())
	email = models.EmailField(max_length=100)
	date_created = models.DateTimeField(auto_now=True)

class BiAnnually(models.Model):
	user = models.OneToOneField(get_user_model())
	email = models.EmailField(max_length=100)
	date_created = models.DateTimeField(auto_now=True)

class Annually(models.Model):
	user = models.OneToOneField(get_user_model())
	email = models.EmailField(max_length=100)
	date_created = models.DateTimeField(auto_now=True)

class Pitch(models.Model):
	user = models.ForeignKey(get_user_model())
	business_name = models.CharField(max_length=100)
	description = models.TextField()
	image = models.ImageField(upload_to='media')
	date_created = models.DateTimeField(auto_now=True)

Levels = (
	('Very High','Very High'),
	('High','High'),
	('Medium','Medium'),
	)
class Portfolio(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	address = models.IntegerField()
	email = models.EmailField()
	cell = models.IntegerField()
	next_of_kin = models.CharField(max_length=100)
	next_of_kin_cell = models.IntegerField()
	website = models.URLField()
	investment_interest = models.DecimalField(max_digits=100,decimal_places=2)
	investments = models.TextField()
	annual_investment_budget = models.DecimalField(max_digits=100,decimal_places=2)
	investment_portfolio = models.FileField(upload_to='media')
	offshore_investments = models.TextField()
	banking_details = models.TextField()
	risk_level = models.CharField(max_length=100,choices = Levels)


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.dispatch import receiver
from django.db.models.signals import post_save
from thorn import ModelEvent, webhook_model
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

@webhook_model
class Personal(models.Model):
	user = models.OneToOneField(get_user_model())
	address = models.TextField()
	category = models.CharField(choices=Category,max_length=100)
	cell = models.IntegerField()
	next_of_kin = models.CharField(max_length=100)
	maritality = models.CharField(max_length=100,choices=Marital_Status)
	banking_details = models.TextField()

	class webhooks:
		on_create = ModelEvent('personal_profile.created')
        on_change = ModelEvent('personal_profile.changed')
        on_delete = ModelEvent('personal_profile.removed')
        on_publish = ModelEvent(
            'personal_profile.published', state__now_eq='PUBLISHED',
        ).dispatches_on_change()

        def payload(self, article):
            return {
                'user': personal.user,
            }

        @models.permalink
        def get_absolute_url(self):
        	return ('blog:article-detail', None, {'uuid': self.uuid})

@webhook_model
class Company(models.Model):
	user = models.OneToOneField(get_user_model())
	name = models.CharField(max_length=100)
	address = models.IntegerField()
	website = models.URLField(max_length=100)
	email = models.EmailField(max_length=100)
	contact = models.TextField()

	class webhooks:
		on_create = ModelEvent('company.created')
		on_change = ModelEvent('company.changed')
        on_delete = ModelEvent('company.removed')
        on_publish = ModelEvent(
            'company.published', state__now_eq='PUBLISHED',
        ).dispatches_on_change()

        def payload(self, article):
            return {
                'user': company,
            }

        @models.permalink
        def get_absolute_url(self):
        	return ('blog:article-detail', None, {'uuid': self.uuid})

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

@webhook_model(
    sender_field='user',
)
class Pitch(models.Model):
	user = models.ForeignKey(get_user_model())
	business_name = models.CharField(max_length=100)
	industry = models.CharField(max_length=100,null=True)
	description = models.TextField()
	image = models.ImageField(upload_to='media')
	date_created = models.DateTimeField(auto_now=True)

	class webhooks:
		on_create = ModelEvent('pitch.created')
		on_change = ModelEvent('pitch.changed')
        on_delete = ModelEvent('pitch.removed')
        on_publish = ModelEvent(
            'pitch.published', state__now_eq='PUBLISHED',
        ).dispatches_on_change()

        def payload(self, article):
            return {
                'user': company,
            }

        @models.permalink
        def get_absolute_url(self):
        	return ('pitch_detail', None, {'uuid': self.uuid})

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

class Conversation(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        message = models.CharField(blank=True, null=True, max_length=225)
        status = models.CharField(blank=True, null=True, max_length=225)
        created_at = models.DateTimeField(auto_now=True)

class Connection(models.Model):
	sender = models.ForeignKey(get_user_model(),related_name='sender')
	receiver = models.ForeignKey(get_user_model(),related_name='receiver')
	date_created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.sender
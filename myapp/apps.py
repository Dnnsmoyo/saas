# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig,apps


class MyappConfig(AppConfig):
    name = 'myapp'
    def ready(self):
    	from actstream import registry
    	registry.register(self.get_model('Personal'),self.get_model('Company'),self.get_model('Daily'),self.get_model('Weekly'),self.get_model('Monthly'),self.get_model('BiAnnually'),self.get_model('Annually'),self.get_model('Pitch'),self.get_model('Portfolio'),apps.get_model('auth','User'))

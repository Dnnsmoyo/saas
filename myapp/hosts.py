from django.conf import settings
from django_hosts import patterns, host
host_patterns = patterns(
    '',
    host(r'investrack', 'something4.urls', name='www'),
    host(r'admin', settings.ROOT_URLCONF, name='admin'),
    host(r'investrack','myapp.urls',name='investrack'),
    host(r'investrack','django.contrib.auth.urls',name='account'),
    host(r'investrack','django_registration.backends.activation.urls',name='register'),
    host(r'investrack','newsletter.urls',name='newsletter'),
    host(r'pricing', 'myapp.urls2', name='pricing'),
    host(r'profile', 'myapp.urls3', name='personal'),
    host(r'profile', 'myapp.urls4', name='company'),

)
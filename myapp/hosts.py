from django.conf import settings
from django_hosts import patterns, host
host_patterns = patterns(
    '',
    host(r'www', 'something4.urls', name='www'),
    host(r'admin', settings.ROOT_URLCONF, name='admin'),
    host(r'pricing', 'myapp.urls2', name='pricing'),
    host(r'profile', 'myapp.urls3', name='personal'),
    host(r'profile', 'myapp.urls4', name='company'),

)
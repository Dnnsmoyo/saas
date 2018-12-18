from django.core.exceptions import PermissionDenied
from .models import Daily,Weekly,Monthly,BiAnnually,Annually

def user_is_daily_sub(function):
    def wrap(request, *args, **kwargs):
        daily = Daily.objects.get(pk=kwargs['daily_id'])
        if daily.user== request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


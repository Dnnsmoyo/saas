from django.conf.urls import url,include
from myapp import views

urlpatterns = [
   #url(r'^$',views.home),
   url(r'^pricing',views.pricing,name='pricing'),
   url(r'^subscribe/daily',views.DailyForm.as_view(),name='daily'),
   url(r'^subscribe/weekly',views.WeeklyForm.as_view(),name='weekly'),
   url(r'^subscribe/monthly',views.MonthlyForm.as_view(),name='monthly'),
   url(r'^subscribe/biannual',views.BiAnnualForm.as_view(),name='biannual'),
   url(r'^subscribe/annual',views.AnnualForm.as_view(),name='annual'),
   ]
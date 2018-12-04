from django.conf.urls import url,include
from myapp import views

urlpatterns = [
   url(r'^$',views.home),
   url(r'^pitch/create$',views.PitchForm.as_view(),name='pitch'),
   url(r'^pitch/all$',views.PitchListView.as_view(),name='pitches'),
   url(r'^api/personal$',views.PersonalList.as_view()),
   url(r'^api/company$',views.CompanyList.as_view()),
   url(r'^api/daily$',views.DailyList.as_view()),
   url(r'^api/weekly$',views.WeeklyList.as_view()),
   url(r'^api/monthly$',views.MonthlyList.as_view()),
   url(r'^api/biannual$',views.BiAnnualList.as_view()),
   url(r'^api/annual$',views.AnnualList.as_view()),
   #url(r'^pricing',views.pricing),
   #url(r'^profile/personal$',views.PersonalForm.as_view(),name='personal'),
   #url(r'^profile/company$',views.CompanyForm.as_view(),name='company'),
]

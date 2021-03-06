from django.conf.urls import url,include
from myapp import views

urlpatterns = [
   url(r'^$',views.home),
   url(r'^connect',views.add_friend),
   url(r'^chat$',views.chat),
   url(r'^conversation$', views.broadcast),
   url(r'^conversations/$', views.conversations),
   url(r'^conversations/(?P<id>[-\w]+)/delivered$',views.delivered),
   url(r'^newsletter/news-list$',views.news_list),
   url(r'^newsletter/(?P<pk>\d+)$',views.news_detail),
   url(r'^newsletter/submission-archive$',views.submission_archive),
   url(r'^newsletter/subscription-activate$',views.subscription_activate),
   url(r'^newsletter/subscription-subscribe$',views.subscription_subscribe),
   url(r'^newsletter/subscription-subscribe-activated',views.subscription_subscribe_activated),
   url(r'^newsletter/subscription-subscribe-email-sent',views.subscription_subscribe_email_sent),
   url(r'^newsletter/subscription-subscribe-user',views.subscription_subscribe_user),
   url(r'^newsletter/subscription-unsubscribe',views.subscription_unsubscribe),
   url(r'^newsletter/subscription-unsubscribe-activated',views.subscription_unsubscribe_activated),
   url(r'^newsletter/subscription-unsubscribe-email-sent',views.subscription_unsubscribe_email_sent),
   url(r'^newsletter/subscription-unsubscribe-user',views.subscription_unsubscribe_user),
   url(r'^leaderboard$',views.leaderboard,name='leaderboard'),
   url(r'^portfolio/new$',views.PortfolioForm.as_view(),name='new_portfolio'),
   url(r'^portfolio/edit(?P<pk>\d+)$',views.PortfolioUpdate.as_view(),name='update_portfolio'),
   url(r'^portfolio/(?P<pk>\d+)$',views.PortfolioDetail.as_view(),name='portfolio_detail'),
   url(r'^portfolio/delete/(?P<pk>\d+)$',views.PortfolioDelete.as_view(),name='delete_portfolio'),
   url(r'^company/edit/(?P<pk>\d+)$',views.CompanyUpdate.as_view(),name='update_company'),
   url(r'^company/delete/(?P<pk>\d+)$',views.CompanyDelete.as_view(),name='delete_company'),
   url(r'^personal/edit/(?P<pk>\d+)$',views.PersonalUpdate.as_view(),name='update_personal'),
   url(r'^personal/delete/(?P<pk>\d+)$',views.PersonalDelete.as_view(),name='delete_personal'),
   url(r'^markets',views.markets),
   #url(r'^receive/pitch$',views.pitch_events),
   url(r'^account/dashboard$',views.user_profile),
   url(r'^api/pitch$',views.PitchList.as_view(),name='pitch_list'),
   url(r'^pitch/(?P<pk>\d+)$',views.PitchDetail.as_view(),name='pitch_detail'),
   url(r'^pitch/edit/(?P<pk>\d+)$',views.PitchUpdate.as_view(),name='update_pitch'),
   url(r'^pitch/delete/(?P<pk>\d+)$',views.PitchDelete.as_view(),name='delete_pitch'),
   url(r'^daily/plan$',views.DailyDetail.as_view(),name='daily_detail'),
   url(r'^weekly/plan$',views.WeeklyDetail.as_view(),name='weekly_detail'),
   url(r'^monthly/plan$',views.MonthlyDetail.as_view(),name='monthly_detail'),
   url(r'^biannual/plan$',views.BiAnnualDetail.as_view(),name='biannual_detail'),
   url(r'^annual/plan$',views.AnnualDetail.as_view(),name='annual_detail'),
   url(r'^api/pitch/(?P<pk>\d+)$',views.PitchDetailView.as_view(),name='detail'),
   url(r'^pitch/create$',views.PitchForm.as_view(),name='pitch'),
   url(r'^pitch/all$',views.PitchListView.as_view(),name='pitches'),
   url(r'^api/personal$',views.PersonalList.as_view()),
   url(r'^api/company$',views.CompanyList.as_view()),
   url(r'^api/daily$',views.DailyList.as_view()),
   url(r'^api/weekly$',views.WeeklyList.as_view()),
   url(r'^api/monthly$',views.MonthlyList.as_view()),
   url(r'^api/biannual$',views.BiAnnualList.as_view()),
   url(r'^api/annual$',views.AnnualList.as_view()),
   url(r'^pricing',views.pricing,name='pricing'),
   url(r'^subscribe/daily',views.DailyForm.as_view(),name='daily'),
   url(r'^subscribe/weekly',views.WeeklyForm.as_view(),name='weekly'),
   url(r'^subscribe/monthly',views.MonthlyForm.as_view(),name='monthly'),
   url(r'^subscribe/biannual',views.BiAnnualForm.as_view(),name='biannual'),
   url(r'^subscribe/annual',views.AnnualForm.as_view(),name='annual'),
   #url(r'^profile/personal$',views.PersonalForm.as_view(),name='personal'),
   url(r'^profile/personal$',views.PersonalForm.as_view(),name='personal'),
   url(r'^profile/company$',views.CompanyForm.as_view(),name='company'),
   #url(r'^pricing',views.pricing),
   #url(r'^profile/personal$',views.PersonalForm.as_view(),name='personal'),
   #url(r'^profile/company$',views.CompanyForm.as_view(),name='company'),
]

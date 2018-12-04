from django.conf.urls import url,include
from myapp import views

urlpatterns = [
   #url(r'^profile/personal$',views.PersonalForm.as_view(),name='personal'),
   url(r'^profile/company$',views.CompanyForm.as_view(),name='company'),
]

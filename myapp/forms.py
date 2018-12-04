from django import forms
from django.forms import ModelForm
from .models import Personal,Company
#from registration.forms import RegistrationForm

class PersonalForm(ModelForm):
	class Meta:
		model = Personal
		fields = '__all__'
		exclude = ['user']

class CompanyForm(ModelForm):
	class Meta:
		model = Company
		fields = '__all__'
		exclude = ['user']


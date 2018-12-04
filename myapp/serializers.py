from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Personal,Company,Daily,Weekly,Monthly,BiAnnually,Annually,Pitch
from django.contrib.auth.models import User

class PersonalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Personal
		fields = '__all__'

		def get_validation_exclusions(self):
			exclusions = super(PersonalSerializer, self).get_validation_exclusions()
			return exclusions + ['user']


class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = '__all__'

		def get_validation_exclusions(self):
			exclusions = super(CompanySerializer, self).get_validation_exclusions()
			return exclusions + ['user']

class DailySerializer(serializers.ModelSerializer):
	class Meta:
		model = Daily
		fields = '__all__'

		def get_validation_exclusions(self):
			exclusions = super(DailySerializer, self).get_validation_exclusions()
			return exclusions + ['user']

class WeeklySerializer(serializers.ModelSerializer):
	class Meta:
		model = Weekly
		fields = '__all__'

		def get_validation_exclusions(self):
			exclusions = super(WeeklySerializer, self).get_validation_exclusions()
			return exclusions + ['user']

class MonthlySerializer(serializers.ModelSerializer):
	class Meta:
		model = Monthly
		fields = '__all__'

		def get_validation_exclusions(self):
			exclusions = super(MonthlySerializer, self).get_validation_exclusions()
			return exclusions + ['user']

class BiAnnualSerializer(serializers.ModelSerializer):
	class Meta:
		model = BiAnnually
		fields = '__all__'

		def get_validation_exclusions(self):
			exclusions = super(BAnnualSerializer, self).get_validation_exclusions()
			return exclusions + ['user']

class AnnualSerializer(serializers.ModelSerializer):
	class Meta:
		model = Annually
		fields = '__all__'

		def get_validation_exclusions(self):
			exclusions = super(AnnualSerializer, self).get_validation_exclusions()
			return exclusions + ['user']

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.shortcuts import render
from django.views import View
from .models import Personal,Company,Daily,Weekly,Monthly,BiAnnually,Annually,Pitch
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import PersonalForm,CompanyForm
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import PersonalSerializer,CompanySerializer,DailySerializer,WeeklySerializer,MonthlySerializer,BiAnnualSerializer,AnnualSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
import datetime
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
paypal_dict = {
    "cmd": "_xclick-subscriptions",
    "business": 'receiver_email@example.com',
    "a3": "9.99",                      # monthly price
    "p3": 1,                           # duration of each unit (depends on unit)
    "t3": "M",                         # duration unit ("M for Month")
    "src": "1",                        # make payments recur
    "sra": "1",                        # reattempt payment on payment error
    "no_note": "1",                    # remove extra notes (optional)
    "item_name": "my cool subscription",
    "notify_url": "http://www.example.com/your-ipn-location/",
    "return": "http://www.example.com/your-return-location/",
    "cancel_return": "http://www.example.com/your-cancel-location/",
}
def home(request):
    current_user = request.user
    if current_user.is_authenticated:
        d = current_user.date_joined
        enddate = pd.to_datetime(d) + pd.DateOffset(days=14)
        return render(request,'index.html',{'enddate':enddate})
    else:
        return render(request,'index.html',{})

class PitchListView(ListView):

    model = Pitch
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super(PitchListView,self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    
@login_required(login_url='/accounts/login/')
def pricing(request):
    #form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    return render(request,'pricing.html')

@login_required(login_url='/accounts/login/')
def user_profile(request):
    person = Personal.objects.filter(user=request.user)
    comp = Company.objects.filter(user=request.user)
    return render(request,'profile.html',{'person':person,'comp':comp})

@method_decorator(login_required, name='dispatch')
class PersonalForm(CreateView):
    template_name = 'myapp/personal_form.html'
    form_class = PersonalForm
    #fields = ['address','category','cell','next_of_kin','maritality','banking_details']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        #action.send(self.request.user, verb='created new project')
        return super(PersonalForm, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class CompanyForm(CreateView):
    template_name = 'myapp/company_form.html'
    form_class = CompanyForm
    #fields = ['name','address','website','email','contact']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        #action.send(self.request.user, verb='created new project')
        return super(CompanyForm, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class DailyForm(CreateView):
    model = Daily
    fields = ['email']
    success_url = '/daily'

    def form_valid(self, form):
        form.instance.user = self.request.user
        #action.send(self.request.user, verb='created new project')
        return super(DailyForm, self).form_valid(form) 

@method_decorator(login_required, name='dispatch')
class WeeklyForm(CreateView):
    model = Weekly
    fields = ['email']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        #action.send(self.request.user, verb='created new project')
        return super(WeeklyForm, self).form_valid(form) 

@method_decorator(login_required, name='dispatch')
class MonthlyForm(CreateView):
    model = Daily
    fields = ['email']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        #action.send(self.request.user, verb='created new project')
        return super(MonthlyForm, self).form_valid(form) 

@method_decorator(login_required, name='dispatch')
class BiAnnualForm(CreateView):
    model = BiAnnually
    fields = ['email']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        #action.send(self.request.user, verb='created new project')
        return super(BiAnnualForm, self).form_valid(form)  

@method_decorator(login_required, name='dispatch')
class AnnualForm(CreateView):
    model = Annually
    fields = ['email']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        #action.send(self.request.user, verb='created new project')
        return super(AnnualForm, self).form_valid(form)    

@method_decorator(login_required, name='dispatch')
class PitchForm(CreateView):
    model = Pitch
    fields = ['business_name','description','image']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        #action.send(self.request.user, verb='created new project')
        return super(PitchForm, self).form_valid(form) 

class PersonalList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, format=None):
        persons = Personal.objects.all()
        serializer = PersonalSerializer(persons, many=True)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PersonalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonalDetail(APIView):
    """
    Retrieve, update or delete a Course instance.
    """
    def get_object(self, pk):
        try:
            return Personal.objects.get(pk=pk)
        except Personal.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Personal = self.get_object(pk)
        serializer = PersonalSerializer(Personal)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Personal = self.get_object(pk)
        serializer = PersonalSerializer(Personal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Personal = self.get_object(pk)
        Personal.delete()
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(status=status.HTTP_204_NO_CONTENT)

class CompanyList(APIView):
    """
    List all Courses, or create a new Course.
    """
    def get(self, request, format=None):
        companies = Companies.objects.all()
        serializer = CompanySerializer(companies, many=True)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CompanySerializer(data=request.data)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyDetail(APIView):
    """
    Retrieve, update or delete a Course instance.
    """
    def get_object(self, pk):
        try:
            return Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Company = self.get_object(pk)
        serializer = CompanySerializer(Company)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Company = self.get_object(pk)
        serializer = CompanySerializer(Company, data=request.data)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Company = self.get_object(pk)
        Company.delete()
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(status=status.HTTP_204_NO_CONTENT)

class DailyList(APIView):
    """
    List all Courses, or create a new Course.
    """
    def get(self, request, format=None):
        dailys = Daily.objects.all()
        serializer = DailySerializer(dailys, many=True)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DailySerializer(data=request.data)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DailyDetail(APIView):
    """
    Retrieve, update or delete a Course instance.
    """
    def get_object(self, pk):
        try:
            return Daily.objects.get(pk=pk)
        except Daily.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Daily = self.get_object(pk)
        serializer = DailySerializer(Daily)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Daily = self.get_object(pk)
        serializer = DailySerializer(Daily, data=request.data)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Daily = self.get_object(pk)
        Daily.delete()
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(status=status.HTTP_204_NO_CONTENT)

class WeeklyList(APIView):
    """
    List all Courses, or create a new Course.
    """
    def get(self, request, format=None):
        weeklys = Weekly.objects.all()
        serializer = WeeklySerializer(weeklys, many=True)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = WeeklySerializer(data=request.data)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WeeklyDetail(APIView):
    """
    Retrieve, update or delete a Course instance.
    """
    def get_object(self, pk):
        try:
            return Weekly.objects.get(pk=pk)
        except Weekly.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Weekly = self.get_object(pk)
        serializer = WeeklySerializer(Weekly)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Weekly = self.get_object(pk)
        serializer = WeeklySerializer(Weekly, data=request.data)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Weekly = self.get_object(pk)
        Weekly.delete()
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(status=status.HTTP_204_NO_CONTENT)

class MonthlyList(APIView):
    """
    List all Courses, or create a new Course.
    """
    def get(self, request, format=None):
        monthlies = Monthly.objects.all()
        serializer = MonthlySerializer(monthlies, many=True)
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MonthlySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MonthlyDetail(APIView):
    """
    Retrieve, update or delete a Course instance.
    """
    def get_object(self, pk):
        try:
            return Monthly.objects.get(pk=pk)
        except Monthly.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Monthly = self.get_object(pk)
        serializer = MonthlySerializer(Monthly)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Monthly = self.get_object(pk)
        serializer = MonthlySerializer(Monthly, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Monthly = self.get_object(pk)
        Monthly.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BiAnnualList(APIView):
    """
    List all Courses, or create a new Course.
    """
    def get(self, request, format=None):
        biannuals = BiAnnually.objects.all()
        serializer = BiAnnualSerializer(biannuals, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BiAnnualSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetail(APIView):
    """
    Retrieve, update or delete a Course instance.
    """
    def get_object(self, pk):
        try:
            return BiAnnually.objects.get(pk=pk)
        except BiAnnually.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        BiAnnually = self.get_object(pk)
        serializer = BiAnnualSerializer(BiAnnually)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        BiAnnually = self.get_object(pk)
        serializer = BiAnnualSerializer(BiAnnually, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        BiAnnually = self.get_object(pk)
        BiAnnually.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AnnualList(APIView):
    """
    List all Courses, or create a new Course.
    """
    def get(self, request, format=None):
        annuals = Annually.objects.all()
        serializer = AnnualSerializer(annuals, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AnnualSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AnnualDetail(APIView):
    """
    Retrieve, update or delete a Course instance.
    """
    def get_object(self, pk):
        try:
            return Annually.objects.get(pk=pk)
        except Annually.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Annually = self.get_object(pk)
        serializer = AnnualSerializer(Annually)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Annually = self.get_object(pk)
        serializer = AnnualSerializer(Annually, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Annually = self.get_object(pk)
        Annually.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






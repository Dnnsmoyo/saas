# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.shortcuts import render
from django.views import View
from .models import Personal,Company,Daily,Weekly,Monthly,BiAnnually,Annually,Pitch,Portfolio,Conversation,Connection
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import PersonalForm,CompanyForm,PortfolioForm
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import PersonalSerializer,CompanySerializer,DailySerializer,WeeklySerializer,MonthlySerializer,BiAnnualSerializer,AnnualSerializer,PitchSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
import datetime
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from actstream import action
from actstream.models import Action
from thorn.django.models import Subscriber
from .decorators import user_is_daily_sub
from django.contrib import messages
from actstream.models import user_stream,actor_stream
from actstream.actions import follow, unfollow
#import the user library
from pusher import Pusher
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404

pusher = Pusher(app_id=u'466128', key=u'c1437bd58d899d4e8957', secret=u'8474154f580fd491e545',cluster=u'ap2')

def home(request):
    current_user = request.user
    act = Action.objects.all()
    #messages.add_message(request, messages.INFO, act)
    if current_user.is_authenticated:
        d = current_user.date_joined
        enddate = pd.to_datetime(d) + pd.DateOffset(days=14)
        return render(request,'index.html',{'enddate':enddate,'act':act})
    else:
        return render(request,'index.html',{'act':act})

def news_list(request):
    return render(request,'newsletter/newsletter_list.html')


def news_detail(request):
    return render(request,'newsletter/newsletter_detail.html')


def submission_archive(request):
    return render(request,'newsletter/submission_archive.html')    


def subscription_activate(request):
    return render(request,'newsletter/subscription_active.html')   


def subscription_subscribe(request):
    return render(request,'newsletter/subscription_subscribe.html')


def subscription_subscribe_activated(request):
    return render(request,'newsletter/subscription_subscribe_activated.html')    


def subscription_subscribe_email_sent(request):
    return render(request,'newsletter/subscription_subscribe_email_sent.html')  


def subscription_subscribe_user(request):
    return render(request,'newsletter/subscription_subscribe_user.html')  


def subscription_unsubscribe(request):
    return render(request,'newsletter/subscription_unsubscribe.html')


def subscription_unsubscribe_activated(request):
    return render(request,'newsletter/subscription_unsubscribe_activated.html')   


def subscription_unsubscribe_email_sent(request):
    return render(request,'newsletter/subscription_unsubscribe_email_sent.html') 


def subscription_unsubscribe_user(request):
    return render(request,'newsletter/subscription_unsubscribe_user.html')


def subscription_update(request):
    return render(request,'newsletter/subscription_update.html') 


def subscription_update_activated(request):
    return render(request,'newsletter/subscription_update_activated.html') 


def subscription_update_email_sent(request):
    return render(request,'newsletter/subscription_update_email_sent.html')        

@login_required(login_url='/accounts/login/')
def chat(request):
    return render(request,"chat.html")

@method_decorator(login_required, name='dispatch')
class PitchForm(CreateView):
    model = Pitch
    fields = ['business_name','description','image','industry']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        action.send(self.request.user, verb='created a pitch')
        #send_mail(
            #subject='Pitch updated',message='You created a pitch instance',from_email ='admin@gmail.com',recipient_list =['dnnsmoyo@gmail.com'],fail_silently=False,)
        return super(PitchForm, self).form_valid(form) 

@method_decorator(login_required, name='dispatch')
class PitchListView(ListView):
    model = Pitch
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super(PitchListView,self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

@method_decorator(login_required, name='dispatch')
class PitchDetail(DetailView):
    model = Pitch

    def get_context_data(self, **kwargs):
        context = super(PitchDetail,self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

@method_decorator(login_required, name='dispatch')
class PitchUpdate(UpdateView):
    model = Pitch
    #action.send(self.request.user, verb='updated a project')
    slug_field = 'business_name'
    fields = ['industry','description','image']
    template_name_suffix = '_update_form'
    success_url = '/'

    
    def form_valid(self, form):
        form.instance.user = self.request.user
        action.send(self.request.user, verb='updated a pitch')
        send_mail('Pitch updated','You updated a pitch instance.','admin@gmail.com',['dnnsmoyo@gmail.com'],fail_silently=False,)
        return super(PitchUpdate, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class PitchDelete(DeleteView):
    model = Pitch
    #action.send(self.request.user, verb='deleted a project')
    slug_field = 'business_name'
    success_url = '/'


    def form_valid(self, form):
        form.instance.user = self.request.user
        action.send(self.request.user, verb='deleted pitch')
        return super(PtchDelete, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class PortfolioForm(CreateView):
    template_name = 'myapp/portfolio_form.html'
    form_class = PortfolioForm
    #fields = ['address','category','cell','next_of_kin','maritality','banking_details']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        action.send(self.request.user, verb='created portfolio')
        return super(PortfolioForm, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class PortfolioDetail(DetailView):
    model = Portfolio

    def get_context_data(self, **kwargs):
        context = super(PortfolioDetail,self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

@method_decorator(login_required, name='dispatch')
class PortfolioUpdate(UpdateView):
    model = Portfolio
    #action.send(self.request.user, verb='updated a project')
    slug_field = 'first_name'
    fields = ['first_name','last_name','address','email','cell','next_of_kin','next_of_kin_cell','website','investment_interest','investments','annual_investment_budget','investment_portfolio','offshore_investments','banking_details','risk_level']
    template_name_suffix = '_update_form'
    success_url = '/'

    
    def form_valid(self, form):
        form.instance.user = self.request.user
        action.send(self.request.user, verb='updated portfolio')
        return super(PortfolioUpdate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class PortfolioDelete(DeleteView):
    model = Portfolio
    #action.send(self.request.user, verb='deleted a project')
    slug_field = 'first_name'
    success_url = '/'


    def form_valid(self, form):
        form.instance.user = self.request.user
        action.send(self.request.user, verb='deleted portfolio')
        return super(PortfolioDelete, self).form_valid(form)

@login_required(login_url='/accounts/login/')
def pricing(request):
    #form = PayPalPaymentsForm(initial=paypal_dict, button_type="subscribe")
    daily = Daily.objects.all()
    weekly = Weekly.objects.all()
    monthly = Monthly.objects.all()
    biannual = BiAnnually.objects.all()
    annual = Annually.objects.all()
    return render(request,'pricing.html',{'daily':daily,'weekly':weekly,'monthly':monthly,'biannual':biannual,'annual':annual})

@login_required(login_url='/accounts/login/')
def user_profile(request):
    person = Personal.objects.filter(user=request.user)
    comp = Company.objects.filter(user=request.user)
    act = actor_stream(request.user)
    user = User.objects.get(username='admin')
    fl = follow(request.user,user)
    return render(request,'profile.html',{'person':person,'comp':comp,'act':act,'fl':fl})

@method_decorator(login_required, name='dispatch')
class PersonalForm(CreateView):
    template_name = 'myapp/personal_form.html'
    form_class = PersonalForm
    #fields = ['address','category','cell','next_of_kin','maritality','banking_details']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        action.send(self.request.user, verb='created personal profile')
        return super(PersonalForm, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class PeronalDetail(DetailView):

    model = Personal
    def get_context_data(self, **kwargs):
        context = super(PersonalDetail,self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

@method_decorator(login_required, name='dispatch')
class PersonalUpdate(UpdateView):
    model = Personal
    #action.send(self.request.user, verb='updated a project')
    slug_field = 'address'
    fields = ['address','category','cell','next_of_kin','maritality','banking_details']
    template_name_suffix = '_update_form'
    success_url = '/'

    
    def form_valid(self, form):
        form.instance.user = self.request.user
        action.send(self.request.user, verb='updated personal profile')
        return super(PersonalUpdate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class PersonalDelete(DeleteView):
    model = Portfolio
    #action.send(self.request.user, verb='deleted a project')
    slug_field = 'address'
    success_url = '/'


    def form_valid(self, form):
        form.instance.user = self.request.user
        action.send(self.request.user, verb='deleted portfolio')
        return super(PersonalDelete, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class CompanyForm(CreateView):
    template_name = 'myapp/company_form.html'
    form_class = CompanyForm
    #fields = ['name','address','website','email','contact']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        action.send(self.request.user, verb='created company profile')
        return super(CompanyForm, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class CompanyDetail(DetailView):
    model = Company

    def get_context_data(self, **kwargs):
        context = super(CompanyDetail,self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

@method_decorator(login_required, name='dispatch')
class CompanyUpdate(UpdateView):
    model = Company
    #action.send(self.request.user, verb='updated a project')
    slug_field = 'name'
    fields = ['name','address','website','email','contact']
    template_name_suffix = '_update_form'
    success_url = '/'

    
    def form_valid(self, form):
        form.instance.user = self.request.user
        action.send(self.request.user, verb='updated company profile')
        return super(CompanyUpdate, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class CompanyDelete(DeleteView):
    model = Company
    #action.send(self.request.user, verb='deleted a project')
    slug_field = 'name'
    success_url = '/'


    def form_valid(self, form):
        form.instance.user = self.request.user
        action.send(self.request.user, verb='deleted company profile')
        return super(CompanyDelete, self).form_valid(form)

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


class PersonalList(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    throttle_scope = 'persons'
    
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
    throttle_scope = 'persons'
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
    throttle_scope = 'companies'
    """
    List all Courses, or create a new Course.
    """
    def get(self, request, format=None):
        companies = Company.objects.all()
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
    throttle_scope = 'companies'
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


class PitchList(APIView):
    throttle_scope = 'pitches'
    """
    List all Courses, or create a new Course.
    """
    def get(self, request, format=None):
        pitches = Pitch.objects.all()
        serializer = PitchSerializer(pitches, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PitchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PitchDetailView(APIView):
    throttle_scope = 'pitches'
    """
    Retrieve, update or delete a Course instance.
    """
    def get_object(self, pk):
        try:
            return Pitch.objects.get(pk=pk)
        except Pitch.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Pitch = self.get_object(pk)
        serializer = PitchSerializer(Pitch)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Pitch = self.get_object(pk)
        serializer = PitchSerializer(Pitch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Pitch = self.get_object(pk)
        Pitch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def leaderboard(request):
    return render(request,'myapp/leaderboard.html')

@csrf_exempt
def broadcast(request):
    message = Conversation(message=request.POST.get('message', ''), status='', user=request.user);
    message.save();
    # create an dictionary from the message instance so we can send only required details to pusher
    message = {'name': message.user.username, 'status': message.status, 'message': message.message, 'id': message.id}
    #trigger the message, channel and event to pusher
    pusher.trigger(u'a_channel', u'an_event', message)
    # return a json response of the broadcasted message
    return JsonResponse(message, safe=False)

    #return all conversations in the database
def conversations(request):
    data = Conversation.objects.all()
    # loop through the data and create a new list from them. Alternatively, we can serialize the whole object and send the serialized response 
    data = [{'name': person.user.username, 'status': person.status, 'message': person.message, 'id': person.id} for person in data]
    # return a json response of the broadcasted messgae
    return JsonResponse(data, safe=False)

    #use the csrf_exempt decorator to exempt this function from csrf checks
@csrf_exempt
def delivered(request, id):
    message = Conversation.objects.get(pk=id);
    # verify it is not the same user who sent the message that wants to trigger a delivered event
    if request.user.id != message.user.id:
        socket_id = request.POST.get('socket_id', '')
        message.status = 'Delivered';
        message.save();
        message = {'name': message.user.username, 'status': message.status, 'message': message.message, 'id': message.id}
        pusher.trigger(u'a_channel', u'delivered_message', message, socket_id)
        return HttpResponse('ok');
    else:
        return HttpResponse('Awaiting Delivery');

@method_decorator(login_required, name='dispatch')
class DailyDetail(TemplateView):
    template_name = 'myapp/daily_detail.html'

  

@method_decorator(login_required, name='dispatch')
class WeeklyDetail(TemplateView):
    template_name = 'myapp/weekly_detail.html'


@method_decorator(login_required, name='dispatch')
class MonthlyDetail(TemplateView):
    template_name = 'myapp/monthly_detail.html'
   

@method_decorator(login_required, name='dispatch')
class BiAnnualDetail(TemplateView):
    template_name = 'myapp/biannual_detail.html'



@method_decorator(login_required, name='dispatch')
class AnnualDetail(TemplateView):
    template_name = 'myapp/annual_detail.html'

def markets(request):
    return render(request,'markets.html')

def add_friend(request):
    users = User.objects.all()
    user = User.objects.get(username)
    Connection.objects.get_or_create(sender=request.user,receiver=user)
    #connect = Connection.objects.create(sender=user,receiver=get_user)
    return HttpResponse("/pitch/list")
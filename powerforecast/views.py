from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from powerforecast.forms import ContactForm, UserForm
from powerforecast.models import *
from powerforecast.forms import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic.edit import FormView, CreateView
from django.views.generic import TemplateView
from django.shortcuts import render
from django_tables2 import RequestConfig
from powerforecast.tables import *
import dataDashboard as dashboard
import time
import datetime
from django.core.exceptions import ValidationError
import json


class Monitor(TemplateView):
    template_name = "monitor.html"

    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        else:
            fore_daily = dashboard.foreDailyMoni()
            fore_mon = dashboard.foreMonMoni()
            context = {'eia':dashboard.eiaMoni(),
                    'pri_forward': dashboard.priceForwardMoni(),
                    'pri_cash': dashboard.priceCashMoni(),
                    'temp_actu': dashboard.tempActMoni(),
                    'pri_avg_mon': dashboard.priceMonthlyAvgMoni(),
                    'temp_fore': dashboard.tempForeMoni(),
                    'fore_output': dashboard.forecastOutputMoni(),
                    'fore_daily': fore_daily[0],
                    'eia_daily': fore_daily[1],
                    'pri_mon': fore_mon[0],
                    'eia_monthly': fore_mon[1]}
            return render(request, self.template_name, context)

class Morris(TemplateView):
    template_name = "morris.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        return super(Morris, self).dispatch(request, *args, **kwargs)

class Flot(TemplateView):
    template_name = "flot.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        return super(Flot, self).dispatch(request, *args, **kwargs)

class General(TemplateView):
    template_name = "general.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        return super(General, self).dispatch(request, *args, **kwargs)

class Icons(TemplateView):
    template_name = "icons.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        return super(Icons, self).dispatch(request, *args, **kwargs)

class Buttons(TemplateView):
    template_name = "buttons.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        return super(Buttons, self).dispatch(request, *args, **kwargs)

class Sliders(TemplateView):
    template_name = "sliders.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        return super(Sliders, self).dispatch(request, *args, **kwargs)

class Timeline(TemplateView):
    template_name = "timeline.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        return super(Timeline, self).dispatch(request, *args, **kwargs)

class Modals(TemplateView):
    template_name = "Modals.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        return super(Modals, self).dispatch(request, *args, **kwargs)

class Widgets(TemplateView):
    template_name = "widgets.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/login/')
        return super(Widgets, self).dispatch(request, *args, **kwargs)
    
class Login(FormView):
    form_class = UserForm
    model = User
    template_name = "login.html"
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = User.objects.get(email=username)
        if user.check_password(password):
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(self.request, user)
                return HttpResponseRedirect('/index/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            return HttpResponseRedirect('/login/')
        return HttpResponseRedirect('/login/')


class Logout(TemplateView):
    template_name = "logout.html"

    def get(self, request):
        # Since we know the user is logged in, we can now just log them out.
        logout(request)

        # Take the user back to the homepage.
        return HttpResponseRedirect('/login/')


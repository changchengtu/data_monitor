#from django.conf.urls.defaults import *
from django.conf.urls import patterns, url
from powerforecast.views import *

urlpatterns = [

    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
    url(r'^monitor/$', Monitor.as_view(), name='monitor'),
    url(r'^morris/$', Morris.as_view(), name='morris'),
    url(r'^flot/$', Flot.as_view(), name='flot'),
    url(r'^general/$', General.as_view(), name='general'),
    url(r'^icons/$', Icons.as_view(), name='icons'),
    url(r'^buttons/$', Buttons.as_view(), name='buttons'),
    url(r'^sliders/$', Sliders.as_view(), name='sliders'),
    url(r'^timeline/$', Timeline.as_view(), name='timeline'),
    url(r'^modals/$', Modals.as_view(), name='modals'),
    url(r'^widgets/$', Widgets.as_view(), name='widgets'),
]

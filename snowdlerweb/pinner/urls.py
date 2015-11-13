from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mode$', views.mode, name='mode'),
    url(r'^(?P<pin>[0-9]+)/pwm/(?P<duty>[0-9]+)$', views.pwm, name='pwm'),
    url(r'^(?P<pin>[0-9]+)/on$', views.on, name='on'),
    url(r'^(?P<pin>[0-9]+)/off$', views.off, name='off'),
]

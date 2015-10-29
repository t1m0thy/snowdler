from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<pin>[0-9]+)/on$', views.on, name='on'),
    url(r'^(?P<pin>[0-9]+)/off$', views.off, name='off'),
]

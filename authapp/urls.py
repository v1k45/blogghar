from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^u/(?P<username>[\w.@+-]+)/$', views.user_profile, name='profile'),
]

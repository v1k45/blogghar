from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^@(?P<username>[\w-]+)/$', views.user_profile, name='profile'),
    url(r'^accounts/profile/', views.profile_redirector, name='user_profile'),
]

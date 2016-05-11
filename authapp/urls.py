from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^@(?P<username>[\w-]+)/$', views.UserProfileView.as_view(), name='profile'),
    url(r'^@(?P<username>[\w-]+)/comments/$', views.UserComments.as_view(), name='user_comments'),
    url(r'^accounts/profile/$', views.profile_redirector, name='user_profile'),
    url(r'^accounts/profile/update/$', views.UserProfileUpdateView.as_view(), name='user_profile_update'),
]

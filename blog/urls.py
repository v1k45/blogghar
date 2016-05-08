from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^@(?P<username>[\w-]+)/blog/$', views.blog_detail, name='user_blog'),
]

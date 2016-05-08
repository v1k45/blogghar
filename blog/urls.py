from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^@(?P<username>[\w-]+)/blog/$', views.blog_detail, name='user_blog'),
    url(r'^blog-home/start/', views.blog_create, name='blog_create'),
    url(r'^blog-home/update/', views.blog_update, name='blog_update'),
]

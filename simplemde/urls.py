from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^upload/$', views.ImageUploadView.as_view(), name='upload'),
    url(r'^md2html/$', views.MarkdownToHTML.as_view(), name='md2html'),
]

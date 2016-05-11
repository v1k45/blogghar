from django.conf.urls import url

from .views import CommentCreateView

urlpatterns = [
    url(r'^post/$', CommentCreateView.as_view(), name='post'),
]

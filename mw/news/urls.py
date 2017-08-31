from django.conf.urls import url
from django.contrib import admin
from news.views import *

urlpatterns = [
    url(r'^articles/$', Articles.as_view(), name='articles'),
    url(r'^articles/(?P<pk>\d+)/$', ArticleDetail.as_view(), name='articledetail'),
]

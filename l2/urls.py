"""l2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin, auth

from blog.views import *

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^delete/comment', delete_comment),
    url(r'^delete/post', delete_post),
    url(r'^profile/', get_profile),
    url(r'^signup/', sign_up),
    url(r'^edit/', edit_post),
    url(r'^view/', show_post),
    url(r'^like/', like),
    url(r'^$', get_posts),
]

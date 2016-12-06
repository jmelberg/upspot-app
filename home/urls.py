from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^signup', views.user_signup),
    url(r'^login', views.user_login),
    url(r'^logout', views.user_logout)
]

from django.conf.urls import  url
from . import views

urlpatterns = [
  url(r'^$', views.map),
  url(r'^spots', views.add_spot),
  url(r'^vehicles', views.add_vehicle),
  url(r'^reserve', views.reserve_spot),
  url(r'^reservations', views.manage_reservations),
]

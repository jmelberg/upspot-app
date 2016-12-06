from django.conf.urls import  url, include
from . import views
from rest_framework import routers
from rest_framework.authtoken import views as token_views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'spots', views.SpotViewSet)
router.register(r'reservations', views.ReservationViewSet)
urlpatterns = [
  url(r'^', include(router.urls)),
  url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
  url(r'^api-token-auth/', token_views.obtain_auth_token)

]

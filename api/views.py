from django.shortcuts import render
from django.contrib.auth.models import User, Group
from park.models import Spot, Reservation
from rest_framework import viewsets
from serializers import UserSerializer, SpotSerializer, ReservationSerializer
from rest_framework.decorators import detail_route
from rest_framework import generics
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import  D


class UserViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows users to be viewed or edited.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer

class SpotViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows spots to be viewed
  """
  serializer_class = SpotSerializer
  queryset = Spot.objects.all()

  def get_queryset(self):
    """
     Handles a get request of spots
     Params: lat, lng, radius**
     Returns: All spots within given radius of search point.
    """
    radius = self.request.GET.get('radius')
    lat = self.request.GET.get('lat')
    lng = self.request.GET.get('lng')
    if not radius:
      radius = 5
    if lat and lng:
      lattitude =  float(lat)
      longitude = float(lng)
      search_point = Point(longitude, lattitude)
      queryset = Spot.objects.filter(
      location__distance_lte=(search_point, D(mi=radius))).annotate(
      distance=Distance('location', search_point)).order_by(
      'distance')
    else:
      queryset = []
    return queryset

class ReservationViewSet(viewsets.ModelViewSet):
  """
  API endpoint that allows reservations to be viewed
  """
  serializer_class = ReservationSerializer
  queryset = Reservation.objects.all()

from django.contrib.auth.models import User, Group
from park.models import Spot, Reservation
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = User
    fields = ('username', 'email')

class SpotSerializer(serializers.ModelSerializer):
  owner = UserSerializer()
  class Meta:
    model = Spot
    fields = ('owner', 'address', 'location', 'available')

class ReservationSerializer(serializers.ModelSerializer):
  spot = SpotSerializer()
  buyer = UserSerializer()
  seller = UserSerializer()
  class Meta:
    model = Reservation
    fields = ('spot', 'price', 'buyer', 'seller', 'start', 'end' )

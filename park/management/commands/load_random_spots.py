from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
from park.models import Spot, User, Reservation, GeoBucket
from park.scripts import geohash_encode, geohash_decode
import random
import sys
from django.core.management.base import BaseCommand


class Command(BaseCommand):
  """
    This command loads 10 spots at random coordinates.
    This is run through the django manage.py script.
    To run: python manage.py load_random_spots
  """
  def handle(self, *args, **options):
    self.populate_spots(10)

  def populate_spots(self, number_of_spots):
    users = User.objects.all()
    for index in range(number_of_spots):
      owner = random.choice(users)
      lattitude = random.uniform(37.32, 37.35)
      longitude = random.uniform(-121.84, -122.00)
      address = "Random spot # {}".format(index)
      new_spot = Spot()
      new_spot.owner = owner
      new_spot.location = Point(longitude, lattitude)
      new_spot.address = address
      new_spot.save()
      # Find geohash to get grid value and retrieve geobucket.
      spot_geohash = geohash_encode(lattitude, longitude)[:6]
      geobucket, created = GeoBucket.objects.get_or_create(geohash=spot_geohash)
      # Add a spot to the given geobucket and save.
      geobucket.spot()
      geobucket.save()

from __future__ import unicode_literals
from django.contrib.gis.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from scripts import geohash_encode, geohash_decode


class Spot(models.Model):
  """
    A spot represents the parking spot for sale.
  """
  owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  address = models.CharField(max_length=100)
  available = models.BooleanField(default=True)
  in_use = models.BooleanField(default=False)
  location = models.PointField()
  sv_location = models.PointField(null=True)
  rating = models.IntegerField(default=0)
  num_ratings = models.IntegerField(default=0)
  num_reservations = models.IntegerField(default=0)
  instructions = models.CharField(max_length=255)
  spot_number = models.CharField(default="", max_length=10)

  def shorthand_address(self):
    """
      Returns street address from address.
      Ex. 841 E Meda, Glendora, CA, US ---> 841 E Meda
    """
    return self.address.split(",")[0]

  def to_miles(self):
    """
    Returns distance in miles
    1 meter = 0.00062137 miles
    """
    return (self.distance.m * 0.00062137)

  def walking_time(self):
    """
      Returns an estimated walking time in minutes from a distance.
      TODO: Add a try catch because distance is an annotated value.
    """
    return int(self.distance.m // 83)

  def lat(self):
    """
      Returns the latitude of the spot location
    """
    return self.location.y

  def lng(self):
    """
      Returns the longitude of the spot location.
    """
    return self.location.x

  def sv_lat(self):
    """
      Returns the latitude of the street view spot location
    """
    return self.sv_location.y

  def sv_lng(self):
    """
      Returns the longitude of the street view spot location.
    """
    return self.sv_location.x

  #TODO Remove from spot as method and add an instance variable of geobucket
  def get_price(self):
    """
      Price is not stored in the spot but fetched from the geobucket which has dynamic pricing.
    """
    geo_bucket = GeoBucket.objects.get(geohash=geohash_encode(self.lat(), self.lng())[:6])
    return geo_bucket.price // 100


class Vehicle(models.Model):
  """
    Vehicles are parked in spots. A user may have multiple vehicles.
  """
  owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  make = models.CharField(max_length=50)
  model = models.CharField(max_length=50)
  license_plate = models.CharField(max_length=20, default="XXXXXXX")


class Reservation(models.Model):
  """
    A reservation is created when a user books a spot.
    Holds info about a certain transaction.
  """
  spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
  price = models.IntegerField()
  buyer = models.ForeignKey(User, related_name="buyer_user")
  seller = models.ForeignKey(User, related_name="seller_user")
  start = models.DateTimeField(blank=True)
  end = models.DateTimeField(blank=True, null=True)

  def checkout(self):
    """
      Function to complete and checkout of the reservation.
    """
    self.end = datetime.datetime.now()
    # TODO add buffer time
    # Release spot back onto market.
    self.spot.available = True
    self.spot.in_use = False
    self.spot.save()

  def closed(self):
    """
      Determines if reservation is closed
    """
    if self.end == None:
      return False
    else:
      return self.end <= timezone.now()

class BuyerProfile(models.Model):
  """
    Because a user may be a buyer and seller of spots we separate profiles into buyer/seller.
    Buyer profile holds info about a user's buying history. Buyers rent spots.
  """
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=35)
  phone_number = models.CharField(max_length=20)
  rating = models.IntegerField(default=0)
  num_ratings = models.IntegerField(default=0)
  num_reservations = models.IntegerField(default=0)

class SellerProfile(models.Model):
  """
    Because a user may be a buyer and seller of spots we separate profiles into buyer/seller.
    Seller profile holds info about a user's history of renting out their spots to others.
  """
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=35)
  phone_number = models.CharField(max_length=20)
  rating = models.IntegerField(default=0)
  num_ratings = models.IntegerField(default=0)
  num_reservations = models.IntegerField(default=0)
  stripe_id = models.CharField(max_length=50)


class GeoBucket(models.Model):
  """
    The GeoBucket model maps to a normal grid system. It allows us to track supply and demand in a given
    square of a grid. This is the model where the price of any given spot is determined.
  """
  geohash = models.CharField(max_length=50)
  spots = models.IntegerField(default=0)
  reservations = models.IntegerField(default=0)
  searches = models.IntegerField(default=0)
  price = models.IntegerField(default=500)
  
  def search(self):
    self.searches += 1

  def spot(self):
    self.spots += 1

  def reservation(self):
    self.reservations += 1
    self.update_price()

  def update_price(self):
    ''' Spot availability hours assumptions
      1.  Get user location
        as location -> spot, price increases
        Use case: Booking from home vs booking from outside

      2.  Surge multiplier is a constant multiplied to the price
        Surge based on spots available/existing
    '''
    fixed_price = 5
    ratio = self.searches / float(self.spots)
    surge = (self.reservations * ratio) / 100 + 1
    return (fixed_price * surge) * 100
  
  # def update_price(self):
  #   """
  #     Function to update price of a given territory.
  #   """
  #   # Calculate searches / spots * reservertions
  #   self.price = 500 + (500 * self.reservations/self.spots)

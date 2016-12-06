import geohash

# Uses Python-geohash for encoding/decoding
def geohash_encode(lat, lng):
  return geohash.encode(lat, lng)

def geohash_decode(geohash):
  return geohash.decode(geohash)

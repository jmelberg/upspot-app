/*
  Read from form address, convert to lat/lng -> geocodeAddress
  args:
    String: address
  return:
    Google Maps LatLng: lat, lng
*/ 
function geocodeAddress(address){
  var location;
  var geocoder = new google.maps.Geocoder();
  geocoder.geocode({'address': address},
    function(results, status) {
      if (status === google.maps.GeocoderStatus.OK) {
        return (new google.maps.LatLng(
          results[0].geometry.location.lat(),
          results[0].geometry.location.lng()));
      }
      else {
        return;
      }
  });
}

/*
  Reverse geocode Address
    Ex: (lat, lng) -> 1 N. Drive, San Francisco, CA, USA
  args:
    Float: lat
    Float: lng
    Function: callback
      reverseGeocode(lat, long, function(result){
        // Do something with result
      });
  return:
    String: address
*/
function reverseGeocode(lat, lng, callback){
  var geocoder = new google.maps.Geocoder();
  var latlng = {lat: lat, lng: lng};
  var address = "";
  geocoder.geocode({'location': latlng}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      if (results[0]) {
        address = results[0].formatted_address;
        callback(address);
      }
      else {
        callback(address);
      }
    }
  });
}

/*
  Places marker on a map
  args:
    Google Map: map
    Google Map Lat/Lng: location
    boolean: draggable
  returns:
    null
*/
function placeMarker(map, location, draggable){
  var p_marker = new google.maps.Marker({
    map: map,
    position: location,
    icon: "https://s3-us-west-2.amazonaws.com/upspot/upspotMarkerSmall.png",
    draggable: draggable
  });
  return p_marker;
}

/*
  Initialize Google Map Street View given HTML element id
  args:
    Google Map Lat/Lng: location
    String: id
    Function: callback
      streetView(location, id, function(result){
        // Do something with result
      });
  return:
    null
*/
function streetViewMap(location, id, callback) {
  var streetView = new google.maps.StreetViewService();
  var panorama = new google.maps.StreetViewPanorama(document.getElementById(id),{});

  streetView.getPanorama({location: location, radius:50}, processStreetViewData);
  function processStreetViewData(data, status) {
    if (status === google.maps.StreetViewStatus.OK) {
      panorama.setPano(data.location.pano);
      var heading = google.maps.geometry.spherical.computeHeading(data.location.latLng,location);
      panorama.setPov({
        heading: heading,
        pitch: 0,
      });
      panorama.setVisible(true);
      callback(panorama);
    }
    else {
      console.log("cannot find");
      return;
    }
  }
}

/*
  Initialize Google Map given HTML element id
  args:
    String: id
    Integer: zoom
  return:
    null
*/










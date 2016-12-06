/*
 * Click the map to set a new location for the Street View camera.
 */

function createReserveMap(lat, lng, sv_lat, sv_lng){
  var mapLocation = new google.maps.LatLng(lat, lng);
  var povLocation = new google.maps.LatLng(sv_lat, sv_lng);
  streetViewMap(povLocation, 'pano', function(result){
      placeMarker(result, povLocation, false);
  });
  // Set up the map.
  var map = new google.maps.Map(document.getElementById('map'), {
    center: mapLocation,
    zoom: 20,
    mapTypeId: google.maps.MapTypeId.HYBRID,
    scrollwheel: false,
    streetViewControl: false
  });

  placeMarker(map, mapLocation, false);

}
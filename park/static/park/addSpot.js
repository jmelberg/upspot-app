jQuery().ready(function() {
  // Street view
  $(".next2").click(function() {
    var location = new google.maps.LatLng(parseFloat($('#Lat').val()), parseFloat($('#Lng').val()));
    streetViewMap(location, 'street_map', function(result){
      $('#street_map').show();
      google.maps.event.trigger(result, 'resize');
      // Add marker
      var svMarker = placeMarker(result, location, true);
      $("#sv_lat").val(svMarker.getPosition().lat());
      $("#sv_lng").val(svMarker.getPosition().lng());
      google.maps.event.addListener(svMarker, 'dragend', function(){
          $("#sv_lat").val(svMarker.getPosition().lat());
          $("#sv_lng").val(svMarker.getPosition().lng());
        });
    });
    $(".counter").text("2 of 3");
    $(".spotform").hide("fast");
    $('#spot2').show();
  });
  // Get Spot number and instructions
  $(".next3").click(function() {
    $(".counter").text("3 of 3");
    $(".spotform").hide("fast");
    $('#spot3').show();
  });

  $(".back1").click(function() {
    $(".counter").text("1 of 3");
    $(".spotform").hide("fast");
    $('#spot1').show();
  });

  $(".back2").click(function() {
    $(".counter").text("2 of 3");
    $(".spotform").hide("fast");
    $('#spot2').show();
  });
});
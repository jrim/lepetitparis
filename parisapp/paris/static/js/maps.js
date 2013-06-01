var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var map;

function initialize() {
  directionsDisplay = new google.maps.DirectionsRenderer();
  var paris = new google.maps.LatLng(48.856614, 2.3522219); 
 var mapOptions = {
    zoom: 6,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    center: paris
  }
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  directionsDisplay.setMap(map);
}

function calcRoute() {
  var startV= document.getElementById('start').value;
  var seperV=startV.split(",");
  var parseV=[parseFloat(seperV[0]),parseFloat(seperV[1])];

  var start = new google.maps.LatLng(parseV[0],parseV[1]);
 
  var endV = document.getElementById('end').value;
   seperV=endV.split(",");
   parseV=[parseFloat(seperV[0]),parseFloat(seperV[1])];

  var end = new google.maps.LatLng(parseV[0],parseV[1]);

  var wayV;
  var waypts = [];
  var wayptv = [];
  var checkboxArray = document.getElementById('waypoints');
  for (var i = 0; i < checkboxArray.length; i++) {
    if (checkboxArray.options[i].selected == true) {
      	wayV = checkboxArray[i].value;
	seperV=wayV.split(",");
	parseV=[parseFloat(seperV[0]),parseFloat(seperV[1])];
	wayptv[i] = new google.maps.LatLng(parseV[0],parseV[1]);
	  waypts.push({ 
	 location:wayptv[i],
          stopover:true});

    }
 }

  var request = {
      origin: start,
      destination: end,
      waypoints: waypts,
      optimizeWaypoints: true,
      travelMode: google.maps.TravelMode.DRIVING
  };
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
      var route = response.routes[0];
      var summaryPanel = document.getElementById('directions_panel');
      summaryPanel.innerHTML = '';
      // For each route, display summary information.
      for (var i = 0; i < route.legs.length; i++) {
        var routeSegment = i + 1;
        summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment + '</b><br>';
        summaryPanel.innerHTML += route.legs[i].start_address + ' to ';
        summaryPanel.innerHTML += route.legs[i].end_address + '<br>';
        summaryPanel.innerHTML += route.legs[i].distance.text + '<br><br>';
      } 
    }
  });
}

google.maps.event.addDomListener(window, 'load', initialize);

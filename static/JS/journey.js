// create the initial directions object, from which the layer
// and inputs will pull data.
var directions = L.mapbox.directions();

console.log(directions);

var directionsLayer = L.mapbox.directions.layer(directions)
    .addTo(map);

var directionsInputControl = L.mapbox.directions.inputControl('inputs', directions)
    .addTo(map);

var directionsErrorsControl = L.mapbox.directions.errorsControl('errors', directions)
    .addTo(map);

var directionsRoutesControl = L.mapbox.directions.routesControl('routes', directions)
    .addTo(map);

var directionsInstructionsControl = L.mapbox.directions.instructionsControl('instructions', directions)
    .addTo(map);

directions.on("load",function(){
	console.log(directions.directions.routes[0].geometry.coordinates);
});

var feature_layer = L.mapbox.featureLayer(); //define the feature layer


function addMarkerLayer(data) { //this will add markers to the map
  startLoading();         // loading screen will start
  feature_layer = L.mapbox.featureLayer(data).addTo(map); //GeoJSON feature objects will be added to the feature_layer, which will be added to the map
  feature_layer.on('click', function(e) {                 //map will zoom into a marker if a user clicks on it
      map.panTo(e.layer.getLatLng());
  });
  map.fitBounds(feature_layer.getBounds());               //position map using bounds of markers
  // feature_layer.on('ready',function(){
  //   feature_layer.on('mouseover', function(e) {
  //     e.layer.openPopup();
  //   });
  //   feature_layer.on('mouseout', function(e) {
  //     e.layer.closePopup();
  //   });
  // });
  // feature_layer.on('ready',function(){
  //   console.log("in ready event");
  //   feature_layer.eachLayer(function(layer) {
  //   // here you call `bindPopup` with a string of HTML you create - the feature
  //   // properties declared above are available under `layer.feature.properties`
  //     console.log("in layers");
  //     var content = '<h2>A ferry ride!<\/h2>' +
  //         '<p>From: ' + layer.feature.properties["title"] + '<br \/>' +
  //         'to: ' + layer.feature.properties["description"] + '<\/p>';
  //     layer.bindPopup(content);
  //   });
  // });
	finishedLoading();
};

$.getJSON('/get_markers', { start_date: [], end_date: [] } ).done(function(data){ //this will load when the user goes to the points of interest page, it will show crimes in the default date range period
    console.log("markers is running");
    addMarkerLayer(data);
  });
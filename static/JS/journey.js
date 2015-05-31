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

var feature_layer = L.mapbox.featureLayer(); //define the feature layer

function addMarkerLayer(data) { //this will add markers to the map
  feature_layer = L.mapbox.featureLayer(data).addTo(map); //GeoJSON feature objects will be added to the feature_layer, which will be added to the map
  feature_layer.on('click', function(e) {                 //map will zoom into a marker if a user clicks on it
      map.panTo(e.layer.getLatLng());
  });
  map.fitBounds(feature_layer.getBounds());               //position map using bounds of markers
  feature_layer.eachLayer(function(layer) {
    // here you call `bindPopup` with a string of HTML you create - the feature
    // properties declared above are available under `layer.feature.properties`
      console.log("in layers");
      var content = '<h1 align="center"><b>' + layer.feature.properties["title"] + '</b><\/h1>' +
          '<p align="center"><b>Description: </b>' + layer.feature.properties["description"] + '<br \/>' +
          '<b>Time: </b>' + layer.feature.properties["time"] + '<br \/>' +
          '<b>Date: </b>' + layer.feature.properties["date"] + '<br \/>' +
          '<b>Address: </b>' + layer.feature.properties["address"] + 
          '<\/p>';
      layer.bindPopup(content);
    });
};

function addFilters() {     //this function will add the filter, and create an event listener that will update the marker points when a user checks or unchecks the filter checkboxes
// Wait until the marker layer is loaded in order to build a list of possible types. If you are doing this with another featureLayer, you should change map.featureLayer to the variable you have assigned to your featureLayer
    // feature_layer.on('ready', function() {
// Collect the types of symbols in this layer. you can also just hardcode an array of types if you know what you want to filter on, like var types = ['foo', 'bar'];
  var typesObj = {}, types = [];
  var features = feature_layer.getGeoJSON().features; //get the features objects from the feature layer
  for (var i = 0; i < features.length; i++) {         //iterate over feature objects, creating a dictionary where the key is the description property of each marker, and the value is true
    typesObj[features[i].properties['title']] = true;
    }

  for (var k in typesObj) types.push(k);            //create a list of the descriptions

  var checkboxes = [];
  // Create a filter interface.
  for (var i = 0; i < types.length; i++) {        //iterate over the descriptions and create DOM div>input objects for each one as a checkbox, and with the id as the description
    // Create an an input checkbox and label inside.
    var item = filters.appendChild(document.createElement('div'));
    var checkbox = item.appendChild(document.createElement('input'));
    var label = item.appendChild(document.createElement('label'));
    checkbox.type = 'checkbox';
    checkbox.id = types[i];
    checkbox.checked = true;
    // create a label to the right of the checkbox with explanatory text
    label.innerHTML = types[i]; 
    label.setAttribute('for', types[i]);
    // Whenever a person clicks on this checkbox, call the update().
    checkbox.addEventListener('change', update);
    checkboxes.push(checkbox);
  };

  // This function is called whenever someone clicks on a checkbox and changes the selection of markers to be displayed.
  function update() {
    console.log("update has been called");
    var enabled = {};
    // Run through each checkbox and record whether it is checked. If it is, add it to the object of types to display, otherwise do not.
    for (var i = 0; i < checkboxes.length; i++) {
      if (checkboxes[i].checked) enabled[checkboxes[i].id] = true;
    }
    feature_layer.setFilter(function(feature) {
      // If this symbol is in the list, return true. if not, return false. The 'in' operator in javascript does exactly that: given a string or number, it says if that is in 
      // a object.
      return (feature.properties['title'] in enabled);
    });
  };
};

function createBuffer (){
	console.log(directions.directions.routes[0].geometry.coordinates);
	console.log(directions.directions.routes[0]);
	// var route_line = turf.linestring([directions.directions.routes[0].geometry.coordinates], { name: 'route_line' } );
	// console.log(route_line);
	var route_line = directions.directions.routes[0];
	var unit = 'miles';
	var buffer_dist = $("#buffer_choice").val();
	console.log(buffer_dist);
	var buffered = turf.buffer(route_line, buffer_dist, unit);
	console.log(buffered);
	var result = turf.featurecollection([buffered, route_line]);
	console.log(result);
	var markers = feature_layer.getGeoJSON();
	console.log(markers);
	var markersWithin = turf.within(markers, buffered);
	console.log(markersWithin);
	feature_layer.setGeoJSON([]);
  try {
	   addMarkerLayer(markersWithin);
     $("#error").empty();
  }
  catch(err){
    $("#error").html("No crimes from previous two weeks in buffer zone selected");
  };
};

$.getJSON('/get_markers', { start_date: [], end_date: [] } ).done(function(data){ //this will load when the user goes to the points of interest page, it will show crimes in the default date range period
    console.log("markers is running");
    startLoading();
    addMarkerLayer(data);
    addFilters();
    finishedLoading();
  });

directions.on("load",function(){
	createBuffer();
	$("#filters").empty(); //empty the filters element so that a new filter list can be created
  addFilters();
});

$("#buffer_choice").change(function(){
	startLoading();
	console.log("buffer changed");
	feature_layer.setGeoJSON([]);
	$.getJSON('/get_markers', { start_date: [], end_date: [] } ).done(function(data){ //this will load when the user goes to the points of interest page, it will show crimes in the default date range period
    console.log("markers is running");
    addMarkerLayer(data);
    debugger;
    createBuffer();
    $("#filters").empty(); //empty the filters element so that a new filter list can be created
    addFilters();
  	});
  	finishedLoading();
});

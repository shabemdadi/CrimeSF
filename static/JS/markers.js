var feature_layer = L.mapbox.featureLayer(); //define the feature layer

var filters = document.getElementById('filters'); //define the filters in the DOM

function addMarkerLayer(data) { //this will add markers to the map
        startLoading();         // loading screen will start
        feature_layer = L.mapbox.featureLayer(data).addTo(map); //GeoJSON feature objects will be added to the feature_layer, which will be added to the map
        feature_layer.on('click', function(e) {                 //map will zoom into a marker if a user clicks on it
            map.panTo(e.layer.getLatLng());
        });
        map.fitBounds(feature_layer.getBounds());               //position map using bounds of markers
        // var features = feature_layer.getGeoJSON().features;
        // for (var i = 0; i < features.length; i++) {
        //    var content = '<p>' + features[i].properties["title"] + '</p>' + // # FIX ME
        //     '<p>' + features[i].properties["description"] + '</p>';
        //     features[i].bindPopup(content);
        // };
};

function addFilters() {     //this function will add the filter, and create an event listener that will update the marker points when a user checks or unchecks the filter checkboxes
// Wait until the marker layer is loaded in order to build a list of possible types. If you are doing this with another featureLayer, you should change map.featureLayer to the variable you have assigned to your featureLayer
    // feature_layer.on('ready', function() {
// Collect the types of symbols in this layer. you can also just hardcode an array of types if you know what you want to filter on, like var types = ['foo', 'bar'];
  var typesObj = {}, types = [];
  var features = feature_layer.getGeoJSON().features; //get the features objects from the feature layer
  for (var i = 0; i < features.length; i++) {         //iterate over feature objects, creating a dictionary where the key is the description property of each marker, and the value is true
    typesObj[features[i].properties['description']] = true;
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
      return (feature.properties['description'] in enabled);
    });
  };
  finishedLoading();
};

$("#marker_button").on("click", function(e) { //this is called when a user submits a date range
    e.preventDefault();
    var start_date = $("input[name='start']").val(); //start and end date from the input fields that were submitted
    var end_date = $("input[name='end']").val();
    console.log("submitted");
    $("#filters").empty(); //empty the filters element so that a new filter list can be created
    $.getJSON('/get_markers', { start_date: start_date, end_date: end_date } ).done(function(data){ //pass in the entered start and end dates and get the GeoJSON objects to be added to the map
      feature_layer.setGeoJSON([]); //empty the feature_layer of objects
      console.log("markers is running");
      addMarkerLayer(data);
      addFilters();
    });
});


$.getJSON('/get_markers', { start_date: [], end_date: [] } ).done(function(data){ //this will load when the user goes to the points of interest page, it will show crimes in the default date range period
    console.log("markers is running");
    addMarkerLayer(data);
    addFilters();
  });

var feature_layer = L.mapbox.featureLayer();

var filters = document.getElementById('filters');

function addMarkerLayer(data) {
        feature_layer = L.mapbox.featureLayer(data).addTo(map);
        feature_layer.on('click', function(e) {
            map.panTo(e.layer.getLatLng());
        });
        map.fitBounds(feature_layer.getBounds());
        // var features = feature_layer.getGeoJSON().features;
        // for (var i = 0; i < features.length; i++) {
        //    var content = '<p>' + features[i].properties["title"] + '</p>' + // # FIX ME
        //     '<p>' + features[i].properties["description"] + '</p>';
        //     features[i].bindPopup(content);
        // };
};

function addFilters() {
// Wait until the marker layer is loaded in order to build a list of possible types. If you are doing this with another featureLayer, you should change map.featureLayer to the variable you have assigned to your featureLayer
    // feature_layer.on('ready', function() {
// Collect the types of symbols in this layer. you can also just hardcode an array of types if you know what you want to filter on, like var types = ['foo', 'bar'];
  var typesObj = {}, types = [];
  var features = feature_layer.getGeoJSON().features;
  for (var i = 0; i < features.length; i++) {
    typesObj[features[i].properties['description']] = true;
    }

  for (var k in typesObj) types.push(k);

  var checkboxes = [];
  // Create a filter interface.
  for (var i = 0; i < types.length; i++) {
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
};

$("#marker_button").on("submit", function() {
    var start_date = $("input[name='start']").val();
    var end_date = $("input[name='end']").val();
    console.log("submitted");
    $.getJSON('/get_markers', { start_date: start_date, end_date: end_date } ).done(function(data){console.log("heat is running");addHeat(data);});
});


$.getJSON('/get_markers', function(data){console.log("markers is running");addMarkerLayer(data);addFilters();});

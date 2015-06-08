$( document ).ready(function(){

    var heat = L.heatLayer([], {    //define heat layer options
        minOpacity: 0, 
        radius: 25,
        blur: 15, 
        maxZoom: 16,
        // max: 0
        // opacity: 0
        // gradient : {1 : 'blue'}
    });

    var feature_layer = L.mapbox.featureLayer();    //define feature layer

    function addHeat(data) {                        
        // Add each marker point to the heatmap.
        feature_layer = L.mapbox.featureLayer(data);    //add features to the feature_layer
        heat.addTo(map);                            //add the heat layer
        feature_layer.on('click', function(e) {     //when clicking on the feature_layer, zoom into that location
            map.panTo(e.layer.getLatLng());
        });
        // Add each marker point to the heatmap.
        feature_layer.eachLayer(function(l) {       //iterate through the features on the feature layer and add those points to the heat map
            heat.addLatLng(l.getLatLng());
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
        NProgress.start();
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
        map.removeLayer(heat);      //remove the heat layer
        heat = L.heatLayer([], {    //redfine the heat layer
            radius: 25,
            blur: 15, 
            maxZoom: 16
        }).addTo(map);
        // Add each marker point to the heatmap.
        feature_layer.eachLayer(function(l) {      //iterate through the features on the feature layer and add those points to the heat map (the features on the layer now will be those checked on filters)
        heat.addLatLng(l.getLatLng());
        });
        NProgress.done();
      };
    };

    $("#heat_button").on("click", function(e) { //this event listener will kick in when a user submits a date range
        NProgress.start();
        e.preventDefault();
        $("#error").removeClass("alert alert-danger"); 
        $("#error").empty();
        var start_date = $("input[name='start']").val(); //define the start and end date
        var end_date = $("input[name='end']").val();
        $("#filters").empty(); //empty the filters element so that a new filter list can be created
        $.getJSON('/get_heat', { start_date: start_date, end_date: end_date } ).done(function(data){ //use a get ajax request and pass in the start and end date to get the GeoJSON features to be added
            map.removeLayer(heat);      //remove the heat layer
            heat = L.heatLayer([], {    //redfine the heat layer
                radius: 25,
                blur: 15, 
                maxZoom: 16
            });
            feature_layer.setGeoJSON([]);   //set the features on the feature_layer to an empty list
            addHeat(data);                  //call the heat function
            addFilters();                   // add filters
            if (feature_layer.getGeoJSON().features.length === 0){ //if there are no crime stats to add to the map
              console.log("in if");
              $("#error").addClass("alert alert-danger"); 
              $("#error").html("No crime stats in range selected");
            };
            NProgress.done();
        });
    });

    $.getJSON('/get_heat', { start_date:[], end_date:[]} ).done(function(data){ //this will be called when the user goes on the heatmap page, it will get the GeoJSON feature objects from the server using our default date range
        startLoading();
        addHeat(data);
        addFilters();
        map.fitBounds(feature_layer.getBounds());  //zoom into the bounds of the features added
        // $(".svg").hide();
        finishedLoading();
    });

    //this adds default values to the form
    $("input[name='start']").attr("value",moment().subtract(15, 'day').format("YYYY-MM-DD"));
    $("input[name='end']").attr("value",moment().format("YYYY-MM-DD"));

    //this will have the tab in the navbar for this page be active
    $('#heat_route').addClass('active');
    $('#markers_route').removeClass('active');
    $('#trends_route').removeClass('active');
    $('#report_route').removeClass('active');
    $('#journey_route').removeClass('active');
    $('#home_route').removeClass('active');
});
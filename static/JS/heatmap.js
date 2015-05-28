var heat = L.heatLayer([], {    //define heat layer options
    minOpacity: 0, 
    radius: 25,
    blur: 15, 
    maxZoom: 16,
    gradient : {1 : 'blue'}
});

var feature_layer = L.mapbox.featureLayer();    //define feature layer

function addHeat(data) {                        
    // Add each marker point to the heatmap.
    startLoading();                             //loading screen will come up
    feature_layer = L.mapbox.featureLayer(data);    //add features to the feature_layer
    console.log(feature_layer);
    heat.addTo(map);                            //add the heat layer
    console.log(heat);
    feature_layer.on('click', function(e) {     //when clicking on the feature_layer, zoom into that location
        map.panTo(e.layer.getLatLng());
    });
    map.fitBounds(feature_layer.getBounds());  //zoom into the bounds of the features added
    // Add each marker point to the heatmap.
    feature_layer.eachLayer(function(l) {       //iterate through the features on the feature layer and add those points to the heat map
        heat.addLatLng(l.getLatLng());
    });
    finishedLoading();
};

$("#heat_button").on("click", function(e) { //this event listener will kick in when a user submits a date range
    e.preventDefault();
    var start_date = $("input[name='start']").val(); //define the start and end date
    var end_date = $("input[name='end']").val();
    var checked_categories = $('input:checkbox:checked').map(function() {
                        return this.value;
                        }).get();
    console.log("submitted");
    $.getJSON('/get_heat', { start_date: start_date, end_date: end_date } ).done(function(data){ //use a get ajax request and pass in the start and end date to get the GeoJSON features to be added
        console.log(data.features);
        // if (data === { "type": "FeatureCollection"}){
        //     console.log("in if");
        //     alert("No crime statistics found in date range entered");
        //     return;
        // };
        console.log("heat is running");
        map.removeLayer(heat);      //remove the heat layer
        heat = L.heatLayer([], {    //redfine the heat layer
            radius: 25,
            blur: 15, 
            maxZoom: 16,
            gradient : {1: 'red'}
        });
        feature_layer.setGeoJSON([]);   //set the features on the feature_layer to an empty list
        addHeat(data);                  //call the heat function
    });
});

$.getJSON('/get_heat', { start_date:[], end_date:[]} ).done(function(data){ //this will be called when the user goes on the heatmap page, it will get the GeoJSON feature objects from the server using our default date range
    console.log("heat is running");
    addHeat(data);
});
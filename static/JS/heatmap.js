var heat = L.heatLayer([], {
    radius: 25,
    blur: 15, 
    maxZoom: 16,
    gradient : {1: 'red'}
});

var feature_layer = L.mapbox.featureLayer();

function addHeat(data) {
    // Add each marker point to the heatmap.
    startLoading();
    feature_layer = L.mapbox.featureLayer(data);
    console.log(feature_layer);
    heat.addTo(map);
    console.log(heat);
    feature_layer.on('click', function(e) {
        map.panTo(e.layer.getLatLng());
    });
    map.fitBounds(feature_layer.getBounds());
    // Add each marker point to the heatmap.
    feature_layer.eachLayer(function(l) {
        heat.addLatLng(l.getLatLng());
    });
    finishedLoading();
};

$("#heat_button").on("click", function(e) {
    e.preventDefault();
    var start_date = $("input[name='start']").val();
    var end_date = $("input[name='end']").val();
    console.log("submitted");
    $.getJSON('/get_heat', { start_date: start_date, end_date: end_date } ).done(function(data){
        console.log("heat is running");
        map.removeLayer(heat);
        heat = L.heatLayer([], {
            radius: 25,
            blur: 15, 
            maxZoom: 16,
            gradient : {1: 'red'}
        });
        feature_layer.setGeoJSON([]);
        addHeat(data);
    });
});

$.getJSON('/get_heat', { start_date:[], end_date:[]} ).done(function(data){
    console.log("heat is running");
    addHeat(data);
});

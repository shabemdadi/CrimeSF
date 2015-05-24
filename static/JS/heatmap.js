var heat = L.heatLayer([], {
    radius: 25,
    blur: 15, 
    maxZoom: 16,
    gradient : {1: 'red'}
}).addTo(map);

function addHeat(data) {
    // Add each marker point to the heatmap.
    feature_layer = L.mapbox.featureLayer(data);
    console.log(data);
    feature_layer.on('click', function(e) {
        map.panTo(e.layer.getLatLng());
    });
    map.fitBounds(feature_layer.getBounds());
    // Add each marker point to the heatmap.
    feature_layer.eachLayer(function(l) {
        heat.addLatLng(l.getLatLng());
    });
    console.log(feature_layer);
};

$("#heat_button").on("submit", function() {
    var start_date = $("input[name='start']").val();
    var end_date = $("input[name='end']").val();
    console.log("submitted");
    $.getJSON('/get_heat', { start_date: start_date, end_date: end_date } ).done(function(data){console.log("heat is running");addHeat(data);});
});


$.getJSON('/get_heat', { start_date:[], end_date:[]} ).done(function(data){console.log("heat is running");addHeat(data);});

var marker = L.marker(new L.LatLng(37.9, -122), {
    icon: L.mapbox.marker.icon({
        'marker-color': 'ff8888'
    }),
    draggable: true
});

marker.bindPopup('This marker is draggable! Move it around.');
marker.addTo(map);

$("#report_form").on("submit", function(e){
	e.preventDefault();
	console.log("form submitted");
});
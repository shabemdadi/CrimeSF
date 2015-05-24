// Provide access token
L.mapbox.accessToken = 'pk.eyJ1Ijoic2hhYmVtZGFkaSIsImEiOiIwckNSMkpvIn0.MeYrWfZexYn1AwdiasXbsg';

// Set up map characteristics and layers
var map = L.mapbox.map('map', 'shabemdadi.fab5eb0c')
        .addLayer(L.mapbox.tileLayer('shabemdadi.fab5eb0c'))
        .addControl(L.mapbox.geocoderControl('mapbox.places', {
        autocomplete: true
            }));
        L.control.locate().addTo(map);

// Set location to be San Francisco

var geocoder = L.mapbox.geocoder('mapbox.places');

geocoder.query('San Francisco, CA', showMap);

function showMap(err, data) {
    // The geocoder can return an area, like a city, or a
    // point, like an address. Here we handle both cases,
    // by fitting the map bounds to an area or zooming to a point.
    if (data.lbounds) {
        map.fitBounds(data.lbounds);
    } else if (data.latlng) {
        map.setView([data.latlng[0], data.latlng[1]], 13);
    }
}

// new L.Control.Zoom({ position: 'topleft' }).addTo(map);

var loader = document.getElementById('loader');

function startLoading() {
    loader.className = '';
};

function finishedLoading() {
    // first, toggle the class 'done', which makes the loading screen
    // fade out
    loader.className = 'done';
    setTimeout(function() {
        // then, after a half-second, add the class 'hide', which hides
        // it completely and ensures that the user can interact with the
        // map again.
        loader.className = 'hide';
    }, 500);
};
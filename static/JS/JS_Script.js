        // Provide access token
        L.mapbox.accessToken = 'pk.eyJ1Ijoic2hhYmVtZGFkaSIsImEiOiIwckNSMkpvIn0.MeYrWfZexYn1AwdiasXbsg';
        
        // Set up map characteristics
        var geocoder = L.mapbox.geocoder('mapbox.places'),
            map = L.mapbox.map('map', 'shabemdadi.fab5eb0c')
                .addLayer(L.mapbox.tileLayer('shabemdadi.fab5eb0c'))
                .addControl(L.mapbox.geocoderControl('mapbox.places'));
        
        // Set location to be San Francisco
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

        var heat = L.heatLayer([], { maxZoom: 12 }).addTo(map);

        $.get('/crime', function(data) {
            console.log(JSON.parse(data));
            console.log("this is running");
            var geojson = L.geoJson(JSON.parse(data), {
                onEachFeature: function(feature, layer) {
                    console.log("this is running");
                    feature.geometry.coordinates.forEach(function(p) {
                        heat.addLatLng(L.latLng(p[0], p[1]));
                    });
                }
            });
        });
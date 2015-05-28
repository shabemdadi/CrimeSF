var heat = L.heatLayer([], {radius: 25, max: 1.0}).addTo(map);

heat.addLatLng([-122,37,0.1]);

console.log(heat);
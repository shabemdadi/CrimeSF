var heat = L.heatLayer([], {minOpacity:0.5, maxZoom:16, max:100000, radius:25}).addTo(map);

var pt = L.latLng(37,-122, 100);

heat.addLatLng(pt);

console.log(heat);
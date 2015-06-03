// var marker = L.marker(new L.LatLng(37.9, -122), {
//     icon: L.mapbox.marker.icon({
//         'marker-color': 'ff8888'
//     }),
//     draggable: true
// });

// marker.bindPopup('This marker is draggable! Move it around.');
// marker.addTo(map);

var feature_layer = L.mapbox.featureLayer(); //define the feature layer

function addMarkerLayer(data) { //this will add markers to the map
  feature_layer = L.mapbox.featureLayer(data).addTo(map); //GeoJSON feature objects will be added to the feature_layer, which will be added to the map
  feature_layer.on('click', function(e) {                 //map will zoom into a marker if a user clicks on it
      map.panTo(e.layer.getLatLng());
  });
  map.fitBounds(feature_layer.getBounds());               //position map using bounds of markers
  feature_layer.eachLayer(function(layer) {
    // here you call `bindPopup` with a string of HTML you create - the feature
    // properties declared above are available under `layer.feature.properties`
      console.log("in layers");
      var content = '<h1 align="center"><b>' + layer.feature.properties["title"] + '</b><\/h1>' +
          '<p align="center"><b>Description: </b>' + layer.feature.properties["description"] + '<br \/>' +
          '<b>Time: </b>' + layer.feature.properties["time"] + '<br \/>' +
          '<b>Date: </b>' + layer.feature.properties["date"] + '<br \/>' +
          '<b>Address: </b>' + layer.feature.properties["address"] + 
          '<\/p>';
      layer.bindPopup(content);
    });
};


// (function () {
//     var date = new Date().toISOString().substring(0, 10),
//         field = $('#report_date');
//     field.value = date;
//     console.log(field.value);

// })()

// var currentTime = new Date()
// var month = currentTime.getMonth() + 1
// var day = currentTime.getDate()
// var year = currentTime.getFullYear()

// $('#report_date').value = month + "/" + day + "/" + year;

$("#report_button").on("click", function(e){
	console.log("form submitted");
	var time = $("input[name='time_input']").val();
	var date = $("input[name='date_input']").val();
	var address = $("input[name='address_input']").val();
	var description = $("textarea[name='description']").val();
	var map_category = $("input[name='crime_category']").val();
	twttr.widgets.load();
	var tweet = "Caution! " + description + " at " + address;
	$("#twitter_icon").attr("data-text", tweet);
	debugger;
	console.log(time);
	console.log(date);
	console.log(address);
	console.log(description);
	console.log(tweet);
	$.getJSON('/report_crime', { time: time, date: date, address: address, description: description, map_category: map_category } ).done(function(data){ //this will load when the user goes to the points of interest page, it will show crimes in the default date range period
    console.log("markers is running");
    feature_layer.setGeoJSON([]); //empty the feature_layer of objects
    addMarkerLayer(data);
  });
});

// $('#b.btn').on('click', function(ev) {
//     ev.preventDefault();
//     // Remove existing iframe
//     $('#tweetBtn iframe').remove();
//     // Generate new markup
//     var tweetBtn = $('<a></a>')
//         .addClass('twitter-share-button')
//         .attr('href', 'http://twitter.com/share')
//         .attr('data-text', tweet)
//         .attr('data-size', 'large')
//         .attr('data-hashtags', 'CrimeSF');
//     $('#tweetBtn').append(tweetBtn);
//     twttr.widgets.load();
// });

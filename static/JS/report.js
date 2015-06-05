
var feature_layer = L.mapbox.featureLayer(); //define the feature layer

function addMarkerLayer(data) { //this will add markers to the map
  feature_layer = L.mapbox.featureLayer(data).addTo(map); //GeoJSON feature objects will be added to the feature_layer, which will be added to the map
  feature_layer.on('click', function(e) {                 //map will zoom into a marker if a user clicks on it
      map.panTo(e.layer.getLatLng());
  });
  // map.fitBounds(feature_layer.getBounds());               //position map using bounds of markers
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

function tweetSetup(custom_text) {
    console.log("tweet setup running");
    $(".twitter-share-button").remove();
    var tweet = $('<a>')
        .attr('href', "https://twitter.com/share")
        .attr('id', "tweet")
        .attr('class', "twitter-share-button")
        .attr("data-size","large")
        .attr("data-hashtags","CrimeSF")
        .text('Tweet');

    $("#tweet_div").append(tweet);
    tweet.attr('data-text', custom_text);
    twttr.widgets.load();
};

$("#report_button").on("click", function(e){
  NProgress.start();
	console.log("form submitted");
	var time = $("input[name='time_input']").val();
	var date = $("input[name='date_input']").val();
	var address = $("input[name='address_input']").val();
	var description = $("textarea[name='description']").val();
	var map_category = $("input[name='crime_category']").val();
	twttr.widgets.load();
	var tweet_text = "Caution! " + description + " at " + address;
  tweetSetup(tweet_text);
	// $("#twitter_icon").attr("data-text", tweet);
	console.log(time);
	console.log(date);
	console.log(address);
	console.log(description);
	console.log(tweet);
	$.getJSON('/report_crime', { time: time, date: date, address: address, description: description, map_category: map_category } ).done(function(data){ //this will load when the user goes to the points of interest page, it will show crimes in the default date range period
    console.log("markers is running");
    feature_layer.setGeoJSON([]); //empty the feature_layer of objects
    addMarkerLayer(data);
    NProgress.done();
  });
});

$("input[name='time_input']").attr("value",moment().format("HH:mm"));
$("input[name='date_input']").attr("value",moment().format("YYYY-MM-DD"));
$("input[name='address_input']").attr("value","683 Sutter Street, San Francisco, CA");
$("textarea[name='description']").html("Pick pocketer");
$("#theft").prop("checked",true);


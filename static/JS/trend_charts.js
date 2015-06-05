// initialize variables
var ctx_time, timeChart, ctx_day, dayChart, ctx_month, monthChart;

// set global chart configurations
var options = {
    animation: false,
    scaleShowGridLines : true,
    scaleLabel: "<%= addCommas(value) %>"};

// Use JSON get requests from flask to define data added into each map, save charts to global variables to that they can be changed with checkboxes

$.getJSON('/get_hour_stats',function(data){
	ctx_time = $("#TimeChart").get(0).getContext("2d"); //get chart element using jQuery
	window.timeChart = new Chart(ctx_time).Line(data,options); //assign graph the data variable returned from the get request
	console.log(data);
});


$.getJSON('/get_day_stats',function(data){
	ctx_day = $("#DayChart").get(0).getContext("2d");
	window.dayChart = new Chart(ctx_day).Line(data,options);
	console.log(data);
});

$.getJSON('/get_month_stats',function(data){
	ctx_month = $("#MonthChart").get(0).getContext("2d");
	window.monthChart = new Chart(ctx_month).Line(data,options);
	console.log(data);
});

function addCommas(nStr)				//have y-axis be formatted with commas
{
    nStr += '';
    x = nStr.split('.');
    x1 = x[0];
    x2 = x.length > 1 ? '.' + x[1] : '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
        x1 = x1.replace(rgx, '$1' + ',' + '$2');
    }
    return x1 + x2;
};


$('input:checkbox').change(function(){ //on changing the checkboxes, empty each graph, gather the checkboxes checked, and recreate charts with new data from get requests
	console.log("checked");
	NProgress.start();
	timeChart.destroy();
	dayChart.destroy();
	monthChart.destroy();
	var map_categories = $('input:checkbox:checked').map(function() { //create JS object with all of the categories checked to pass to get requests
                        return this.value;
                        }).get();
	console.log(typeof(map_categories));
	console.log(map_categories);
	$.getJSON('/get_hour_stats', { map_categories: JSON.stringify(map_categories) } ).done(function(data){ //make JS object a string to pass into get request
		var ctx_time = $("#TimeChart").get(0).getContext("2d");
		var timeChart = new Chart(ctx_time).Line(data,options);
		console.log(data);
	});

	$.getJSON('/get_day_stats', { map_categories: JSON.stringify(map_categories) } ).done(function(data){
		var ctx_day = $("#DayChart").get(0).getContext("2d");	
		var dayChart = new Chart(ctx_day).Line(data,options);
		console.log(data);
	});

	$.getJSON('/get_month_stats', { map_categories: JSON.stringify(map_categories) } ).done(function(data){
		var ctx_month = $("#MonthChart").get(0).getContext("2d");
		var monthChart = new Chart(ctx_month).Line(data,options);
		console.log(data);
	});
	NProgress.done();
});


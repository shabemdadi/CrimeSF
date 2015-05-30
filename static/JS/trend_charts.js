// Get context with jQuery - using jQuery's .get() method.
var ctx_time, timeChart, ctx_day, dayChart, ctx_month, monthChart;

// Use JSON get requests from flask to define data added into each map

var options = {
    animation: false,
    scaleShowGridLines : true,
    scaleLabel: "<%= addCommas(value) %>"};

$.getJSON('/get_hour_stats',function(data){
	ctx_time = $("#TimeChart").get(0).getContext("2d");
	window.timeChart = new Chart(ctx_time).Line(data,options);
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

function addCommas(nStr)
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


$('input:checkbox').change(function(){
	console.log("checked");
	timeChart.destroy();
	dayChart.destroy();
	monthChart.destroy();
	var map_categories = $('input:checkbox:checked').map(function() {
                        return this.value;
                        }).get();
	console.log(typeof(map_categories));
	console.log(map_categories);
	$.getJSON('/get_hour_stats', { map_categories: JSON.stringify(map_categories) } ).done(function(data){
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
});


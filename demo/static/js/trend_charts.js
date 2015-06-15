// initialize variables
var ctx_time, timeChart, ctx_day, dayChart, ctx_month, monthChart;

// set global chart configurations
var options = {
    animation: false,
    scaleShowGridLines : true,
    scaleLabel: "<%= addCommas(value) %>",
    // multiTooltipTemplate: "<%= addCommas(value) %>",
    tooltipTemplate: "<%if (label){%><%=label%>: <%}%><%= addCommas(value) %>",
    responsive: true,
	datasetFill : false,
    scaleShowLabels: false,
	"lineAtIndex": 2};

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

//this will apply a vertical line to the chart for this point in time
Chart.types.Line.extend({
    name: "LineWithLine",
    initialize: function () {
        Chart.types.Line.prototype.initialize.apply(this, arguments);
    },
    draw: function () {
        Chart.types.Line.prototype.draw.apply(this, arguments);
        
        var point = this.datasets[0].points[this.options.lineAtIndex]
        var scale = this.scale

        // draw line
        this.chart.ctx.beginPath();
        this.chart.ctx.moveTo(point.x, scale.startPoint + 24);
        this.chart.ctx.strokeStyle = '#ff0000';
        this.chart.ctx.lineTo(point.x, scale.endPoint);
        this.chart.ctx.stroke();
        
        // write NOW
        this.chart.ctx.textAlign = 'center';
        this.chart.ctx.fillText("NOW", point.x, scale.startPoint + 12);
    }
});

//get the current hour, day, month to be used to put the vertical line on each chart
var hour_list = ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00",
                  "16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00"]
var hour = moment().format("HH:00");
var line_index_hour = hour_list.indexOf(hour);

var day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
var day = moment().format("dddd");
var line_index_day = day_list.indexOf(day);

var month_list = ["January","February","March","April","May","June","July","August","September","October","November","December"]
var month = moment().format("MMMM");
var line_index_month = month_list.indexOf(month);

// Use JSON get requests from flask to define data added into each map, save charts to global variables to that they can be changed with checkboxes

$.getJSON('/get_hour_stats',function(data){
	ctx_time = $("#TimeChart").get(0).getContext("2d"); //get chart element using jQuery
	options["lineAtIndex"] = line_index_hour;		//change chart configuration to put the vertical line at this hour
	window.timeChart = new Chart(ctx_time).LineWithLine(data,options); //assign graph the data variable returned from the get request
});


$.getJSON('/get_day_stats',function(data){
	ctx_day = $("#DayChart").get(0).getContext("2d");
	options["lineAtIndex"] = line_index_day;
	window.dayChart = new Chart(ctx_day).LineWithLine(data,options);
});

$.getJSON('/get_month_stats',function(data){
	ctx_month = $("#MonthChart").get(0).getContext("2d");
	options["lineAtIndex"] = line_index_month;
	window.monthChart = new Chart(ctx_month).LineWithLine(data,options);
});

$('input:checkbox').change(function(){ //on changing the checkboxes, empty each graph, gather the checkboxes checked, and recreate charts with new data from get requests
	NProgress.start();
	timeChart.destroy();
	dayChart.destroy();
	monthChart.destroy();
	var map_categories = $('input:checkbox:checked').map(function() { //create JS object with all of the categories checked to pass to get requests
                        return this.value;
                        }).get();
	$.getJSON('/get_hour_stats', { map_categories: JSON.stringify(map_categories) } ).done(function(data){ //make JS object a string to pass into get request
		var ctx_time = $("#TimeChart").get(0).getContext("2d");
		options["lineAtIndex"] = line_index_hour;
		var timeChart = new Chart(ctx_time).LineWithLine(data,options);
	});

	$.getJSON('/get_day_stats', { map_categories: JSON.stringify(map_categories) } ).done(function(data){
		var ctx_day = $("#DayChart").get(0).getContext("2d");	
		options["lineAtIndex"] = line_index_day;
		var dayChart = new Chart(ctx_day).LineWithLine(data,options);
	});

	$.getJSON('/get_month_stats', { map_categories: JSON.stringify(map_categories) } ).done(function(data){
		var ctx_month = $("#MonthChart").get(0).getContext("2d");
		options["lineAtIndex"] = line_index_month;
		var monthChart = new Chart(ctx_month).LineWithLine(data,options);
	});
	NProgress.done();
});

//this will have the tab in the navbar for this page be active
$('#heat_route').removeClass('active');
$('#markers_route').removeClass('active');
$('#trends_route').addClass('active');
$('#report_route').removeClass('active');
$('#journey_route').removeClass('active');
$('#home_route').removeClass('active');


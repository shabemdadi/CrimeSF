// Get context with jQuery - using jQuery's .get() method.
var ctx_time = $("#TimeChart").get(0).getContext("2d");
var ctx_day = $("#DayChart").get(0).getContext("2d");
var ctx_month = $("#MonthChart").get(0).getContext("2d");
// Use JSON get requestts from flask to define data added into each map
// startLoading();	//start loading page

$.getJSON('/get_hour_stats',function(data){
	var timeChart = new Chart(ctx_time).Line(data);
	console.log(data);
});

$.getJSON('/get_day_stats',function(data){
	var dayChart = new Chart(ctx_day).Line(data);
	console.log(data);
});

$.getJSON('/get_month_stats',function(data){
	var monthChart = new Chart(ctx_month).Line(data);
	console.log(data);
});

// finishedLoading(); //fade out loading page
// var data = {
//     labels: ["January", "February", "March", "April", "May", "June", "July"],
//     datasets: [
//         {
//             label: "My First dataset",
//             fillColor: "rgba(220,220,220,0.2)",
//             strokeColor: "rgba(220,220,220,1)",
//             pointColor: "rgba(220,220,220,1)",
//             pointStrokeColor: "#fff",
//             pointHighlightFill: "#fff",
//             pointHighlightStroke: "rgba(220,220,220,1)",
//             data: [65, 59, 80, 81, 56, 55, 40]
//         }
//     ]
// };

// myLineChart.addData([40, 60], "August");


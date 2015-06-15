> Learn more about the developer by visiting her [LinkedIn](https://www.linkedin.com/in/shabnamemdadi).

#Crime SF

CrimeSF is an interactive crime mapping app that seeks to analyze and present the massive amount of available crime statistics in a digestive manner for users. The app allows users to customize the data shown in maps and data graphics to what is most useful to them. Users have the opportunity to contribute to the platform, reporting incidents they witness, updating the app in real-time. Finally, the app allows users to take advantage of crime data in route planning, showing users crime incidents around their journey to a destination and allowing them to bypass these hotspots by setting alternative routes.

This app was built in 4.5 weeks during the Spring 2015 cohort of Hackbright Academy's Software Engineering Fellowship.

####Technology Stack

**Backend:**  

+ Python
+ Flask
+ SQLAlchemy 
+ SQLite
+ PostgreSQL

**Frontend:** 

+ JavaScript, jQuery, AJAX 
+ HTML, Bootstrap, CSS, Jinja
+ Turf.js, Leaflet-heat.js
+ Chart.js
+ twitter-widgets.js

**APIs:**
+ Mapbox
+ Socrata Open Data

##Overview
+ Seed database with crime statistics from [SF OpenData]( https://data.sfgov.org/) using the [Socrata Open Data API](http://dev.socrata.com/)
+ Call data API for daily updated crime statistics not already in our database
+ Use AJAX calls to query database holding crime statistics to send to graphics
+ For Maps:
  * Create GeoJSON feature objects with query results to be sent to the map
  * Use Mapbox API to display various types of maps
+ For Trend Graphs:
  * Create graph data points from query results to be sent to trend graphs
  * Use Charts.js to render the trend graphs
+ For User Routing:
  * Use Mapbox Directions API to route users from origin to destination
  * Use Turf.js to create buffer zone around route
  * Query database to present crime incidents within buffer zone shown
+ For User Reporting:
  * Update database with user reported crime
  * Use Mapbox Geocoder API to add marker to map where user has reported incident
  * Use twitter-widgets.js to create Twitter button sending user to their Twitter with pre-generated tweet containing the description and address of the crime they have just reported
	
###Features

####Homepage

<img align="center" src="/static/images/Homepage.png" alt="Homepage">


####Heatmap

+ Uses a default date range of crime statistics within the past two weeks
+ User can specify a customized date range for the incidents shown
+ Filter allows the user to customize what type of crime incidents they would like to see

<img align="center" src="/static/images/Heatmap.png" alt="Heatmap">


####Points of Interest

+ Uses a default date range of crime statistics within the past two weeks
+ Upon clicking on a marker, more information regarding a crime incident will be presented
+ User can specify a customized date range for the incidents shown
+ Filter allows the user to customize what type of crime incidents they would like to see

<img align="center" src="/static/images/Points_of_Interest.png" alt="points_of_interest">


####Trends

+ Shows levels of crime by hour, day of week, and month
+ Filter allows the user to customize what type of crime incidents they would like to see
+ Charts denote the current position of the user

<img align="center" src="/static/images/Trend_Hour.png" alt="trend_hour">

<img align="center" src="/static/images/Trend_Day.png" alt="trend_day">

<img align="center" src="/static/images/Trend_Month.png" alt="trend_month">

####Your Journey

+ Shows crime incidents within the past two weeks
+ Users can specify an origin and a destination either by clicking on the map or by entering them into the origin and destination fields
+ Users can select their mode of transport (walking, driving, biking)
+ A route will be generated for the user, showing crime incidents within a default buffer zone of 0.1 miles from the route
+ Types of crimes are shown with a filter, and filter can be updated by user
+ Users can customize the route to avoid crime incidents by clicking and dragging points on the route

<img align="center" src="/static/images/Journey_Default.png" alt="journey_default">

<img align="center" src="/static/images/Journey_Buffer.png" alt="journey_buffer">

####Report

+ Allows users to report crime incidents in real time
+ When user has completed all form fields and submitted, they can click on the twitter button which will connect them to their Twitter along with a pre-generated tweet of the crime incident they have reported
+ Once the form is submitted, a point of interest marker will be shown on the map at the address given
+ The same crime incident cannot be submitted again (to avoid multiple users reporting the same incident)

<img align="center" src="/static/images/Report.png" alt="Report">

<img align="center" src="/static/images/Report_Tweet.png" alt="Report_Tweet">


##Get CrimeSF Running on Your Machine

Clone or fork this repo: 

```
https://github.com/shabemdadi/CrimeSF.git

```

Create and activate a virtual environment inside your project directory: 

```

virtualenv env

source env/bin/activate

```

Install the requirements:

```
pip install -r requirements.txt

```
Create the database:

```
python -i model.py
db.create_all()

```

Seed data:

```

python server.py

```

Navigate to `localhost:5000` to find out about crime in your city!


##Looking Ahead

Deployment coming soon!

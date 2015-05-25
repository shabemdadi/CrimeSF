from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import Crime_Stat, Data_Import, connect_to_db, db
import json
import decimal
import requests
from sqlalchemy import desc
import csv
from datetime import datetime, timedelta

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
   
    return render_template("homepage.html")


@app.route('/points-of-interest')
def show__markers():
    """Show map with markers."""

    return render_template("markers.html")


@app.route('/get_markers')
def get_marker_points():
    """Get JSON objects for marker points."""

    marker_color_dict = {'Personal Theft/Larceny':'#FF0000',    #This dictionary will link the type of crime to the color marker it will be assigned    
                                'Robbery':'#0000FF',
                                'Rape/Sexual Assault':'#008000',
                                'Aggravated Assault':'#FFA500',
                                'Simple Assault':'#6600CC',
                                'Other':'#669999',
                            }

    start_date = request.args.get("start_date") #start_date and end_date are defined in the event listener in javascript and passed into Flask
    print start_date
    end_date = request.args.get("end_date")

    if start_date:                              #if the user enters in a start_date

        print "start_date has been posted"

        start_date_formatted = datetime.strptime(start_date,"%Y-%m-%d") #reformat start and end dates as date objects
        end_date_formatted = datetime.strptime(end_date,"%Y-%m-%d")

        crime_stats = Crime_Stat.query.filter(Crime_Stat.date >= start_date_formatted, Crime_Stat.date <= end_date_formatted).limit(100).all() #query database for crime stats between start and end date
        marker_object_dict = { "type": "FeatureCollection"}
        marker_object_list = []

        marker_symbol_dict = {}

        if crime_stats:     #if there are crime stats between those dates, iterate over them and create the JSON object that will be passed into Mapbox
        
            for crime in crime_stats:           # need to add in address
                marker_object = {
                                "type": "Feature",
                                "geometry": {
                                  "type": "Point",
                                  "coordinates": [str(decimal.Decimal(crime.x_cord)), str(decimal.Decimal(crime.y_cord))] #FIX ME
                                },
                                "properties": {
                                  "title": "Mapbox DC",
                                  "description": crime.map_category,
                                  "marker-color": marker_color_dict[crime.map_category],
                                  "marker-size": "small",
                                  "marker-symbol": "marker"
                                }
                              }

                marker_object_list.append(marker_object)              

            marker_object_dict["features"] = marker_object_list    

            return jsonify(marker_object_dict)

        else:                               # FIX ME - create code for dealing with no stats in the period the user designates

            flash("No crime statistics found in date range entered")
            return jsonify({})

    else:                               # user has not entered in a date, use a default period of 45 days ago
        
        end_date = datetime.now()                    
        start_date = end_date - timedelta(days=45)

        print start_date
        print "start_date has been posted"

        # start_date_formatted = datetime.strptime(start_date,"%Y-%m-%d %H:%M:%S")
        # end_date_formatted = datetime.strptime(end_date,"%Y-%m-%d %H:%M:%S")

        crime_stats = Crime_Stat.query.filter(Crime_Stat.date >= start_date, Crime_Stat.date <= end_date).limit(100).all()
        marker_object_dict = { "type": "FeatureCollection"}
        marker_object_list = []

        marker_symbol_dict = {}
        
        for crime in crime_stats:           # need to add in address
            marker_object = {
                            "type": "Feature",
                            "geometry": {
                              "type": "Point",
                              "coordinates": [str(decimal.Decimal(crime.x_cord)), str(decimal.Decimal(crime.y_cord))] #FIX ME
                            },
                            "properties": {
                              "title": "Mapbox DC",
                              "description": crime.map_category,
                              "marker-color": marker_color_dict[crime.map_category],
                              "marker-size": "small",
                              "marker-symbol": "marker"
                            }
                          }

            marker_object_list.append(marker_object)              

        marker_object_dict["features"] = marker_object_list    

        return jsonify(marker_object_dict)

@app.route('/heat')
def show_heat():
    """Show heatmap"""

    return render_template("heatmap.html")

    
@app.route('/get_heat')
def get_heat_points():
    """Make JSON objects for markers on heatmap."""

    start_date = request.args.get("start_date") #start and end dates are defined in the event listener in JS when user selects date range
    print start_date
    end_date = request.args.get("end_date")

    if start_date:                              #if the user has selected a date range

        print "start_date has been posted"

        start_date_formatted = datetime.strptime(start_date,"%Y-%m-%d") #reformat start and end date as date objects
        end_date_formatted = datetime.strptime(end_date,"%Y-%m-%d")

        crime_stats = Crime_Stat.query.filter(Crime_Stat.date >= start_date_formatted, Crime_Stat.date <= end_date_formatted).limit(200).all() #query database for crime stats in user selected date range
        marker_object_dict = { "type": "FeatureCollection"}
        marker_object_list = []

        marker_symbol_dict = {}

        if crime_stats:                         #iterate through the crime_stats to create JSON feature objects that will be passed into Mapbox
        
            for crime in crime_stats:           # need to add in address
                marker_object = {
                                "type": "Feature",
                                "geometry": {
                                  "type": "Point",
                                  "coordinates": [str(decimal.Decimal(crime.x_cord)), str(decimal.Decimal(crime.y_cord))] #FIX ME
                                },
                                "properties": {
                                  "title": "Mapbox DC",
                                  "description": crime.map_category,
                                  "marker-color": '#FF0000',
                                  "marker-size": "small",
                                  "marker-symbol": "marker"
                                }
                              }

                marker_object_list.append(marker_object)              

            marker_object_dict["features"] = marker_object_list    

            return jsonify(marker_object_dict)

        else: #FIX ME - write code to deal with no crime stats found in user selected range

            flash("No crime statistics found in date range entered")
            return jsonify(marker_object_dict)

    else:       #user has not selected a range, use this year as default period

        end_date = datetime.now()                    
        beginning_year = "%s-01-01" % end_date.year
        start_date = datetime.strptime(beginning_year,"%Y-%m-%d")

        print start_date
        print "start_date has been posted"

        # start_date_formatted = datetime.strptime(start_date,"%Y-%m-%d %H:%M:%S")
        # end_date_formatted = datetime.strptime(end_date,"%Y-%m-%d %H:%M:%S")

        crime_stats = Crime_Stat.query.filter(Crime_Stat.date >= start_date, Crime_Stat.date <= end_date).limit(100).all()
        marker_object_dict = { "type": "FeatureCollection"}
        marker_object_list = []

        marker_symbol_dict = {}
        
        for crime in crime_stats:           # need to add in address
            marker_object = {
                            "type": "Feature",
                            "geometry": {
                              "type": "Point",
                              "coordinates": [str(decimal.Decimal(crime.x_cord)), str(decimal.Decimal(crime.y_cord))]
                            },
                            "properties": {
                              "title": crime.description,
                              "description": crime.map_category, 
                              "address": crime.address, 
                               "date": datetime.strftime(crime.date, "%m/%d/%Y"), 
                               "time": "time placeholder", #FIX ME 
                               "day-of-week": crime.day_of_week,
                              "marker-color": '#FF0000',
                              "marker-size": "small",
                              "marker-symbol": "marker"
                            }
                          }

            marker_object_list.append(marker_object)            

        marker_object_dict["features"] = marker_object_list    

        return jsonify(marker_object_dict)

@app.route('/trends')
def show_charts():
    """Show trend line graphs"""

    return render_template("charts.html")


@app.route('/get_hour_stats')
def get_hour_stats():
    """Get hour data to be rendered on charts.js"""

    unique_hours = Crime_Stat.query.group_by(Crime_Stat.hour).order_by(Crime_Stat.hour).all() #create a list of the unique hours represented in the database
    data_point_list = []
    label_list = []

    for hour in unique_hours:       #iterate over each hour, and query the database to find the count of crimes happening in each hour. The count will be the datapoint for that hour.
        count_crimes = len(Crime_Stat.query.filter_by(hour=hour.hour).all())
        data_point_list.append(count_crimes)
        label_list.append(hour.hour)

    data = {"labels": [label_list], "datasets": [   #this is the data variable that will be passed into the graph
        {"label": "My First dataset",
        "fillColor": "rgba(220,220,220,0.2)",
        "strokeColor": "rgba(220,220,220,1)",
        "pointColor": "rgba(220,220,220,1)",
        "pointStrokeColor": "#fff",
        "pointHighlightFill": "#fff",
        "pointHighlightStroke": "rgba(220,220,220,1)",
        "data": [data_point_list]}]
        }

    print jsonify(data)    
    return jsonify(data)

@app.route('/get_day_stats')
def get_day_stats():
    """Get day data to be rendered on charts.js"""

    data_point_list = []
    label_list = []
    day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    for day in day_list:    #iterate through each day, finding the count of crimes occurring on that day and making that count the datapoint for that day
        count_crimes = len(Crime_Stat.query.filter_by(day_of_week=day).all())
        label_list.append(day)
        data_point_list.append(count_crimes)

    data = {"labels": [label_list], "datasets": [   #This is the data variable that will be passed into the graph
        {"label": "My First dataset",
        "fillColor": "rgba(220,220,220,0.2)",
        "strokeColor": "rgba(220,220,220,1)",
        "pointColor": "rgba(220,220,220,1)",
        "pointStrokeColor": "#fff",
        "pointHighlightFill": "#fff",
        "pointHighlightStroke": "rgba(220,220,220,1)",
        "data": [data_point_list]}]
        }

    print data
    print jsonify(data)    
    return jsonify(data)

@app.route('/get_month_stats')
def get_month_stats():
    """Get month data to be rendered on charts.js"""

    data_point_list = []
    label_list = []
    month_list = ["January","February","March","April","May","June","July","August","September","October","November","December"]

    for month in month_list:             #iterate through each month, finding the count of crimes occurring in that month and making that count the datapoint for that month
        count_crimes = len(Crime_Stat.query.filter_by(month=month).all())
        label_list.append(month)
        data_point_list.append(count_crimes)

    data = {"labels": [label_list], "datasets": [   #This is the data variable that will be passed into the graph
        {"label": "My First dataset",
        "fillColor": "rgba(220,220,220,0.2)",
        "strokeColor": "rgba(220,220,220,1)",
        "pointColor": "rgba(220,220,220,1)",
        "pointStrokeColor": "#fff",
        "pointHighlightFill": "#fff",
        "pointHighlightStroke": "rgba(220,220,220,1)",
        "data": [data_point_list]}]
        }

    print data
    print jsonify(data)    
    return jsonify(data)

@app.route('/journey')
def get_route():
    """Show routing map"""

    date_now = datetime.now()                                       #Show current date and time
    date_formatted = datetime.strftime(date_now,"%A, %B %d, %Y")
    time_formatted = datetime.strftime(date_now, "%H:%M")

    return render_template("journey.html",date=date_formatted, time=time_formatted)

@app.route('/get_recent')  #This will happen when the user clicks on the "Get Recent Stats" button, it will update our database with the same function used in our seed file
def get_recent_stats():
    """Check API to see if there are new crime stats, if so, import into database."""

    print "refresh started"

    map_category_dict = {'LARCENY/THEFT':'Personal Theft/Larceny',
                 'BURGLARY':'Robbery',
                 'SEX OFFENSES, FORCIBLE':'Rape/Sexual Assault',
                 'VEHICLE THEFT':'Personal Theft/Larceny',
                 'ROBBERY':'Personal Theft/Larceny',
                 'STOLEN PROPERTY':'Personal Theft/Larceny',
                 'SEX OFFENSES, NON FORCIBLE':'Rape/Sexual Assault'
                 }

    recent_import_date = Data_Import.query.order_by(desc(Data_Import.max_date)).first().max_date

    recent_import_date_formatted = recent_import_date.strftime('%Y-%m-%dT%H:%M:%S')

    data = requests.get("https://data.sfgov.org/resource/gxxq-x39z.csv?$WHERE=date>='%s'&$$app_token=RvFtAMemRY6per3vRmUEutOfM" % recent_import_date_formatted)

    data_text = data.text

    reader = csv.reader(data_text.splitlines(), delimiter='\t')

    for i, row in enumerate(reader):
        newrow = row[0].strip("'")
        newrow_split = newrow.split(",")
        if i > 0:
            try:
                overlap = Crime_Stat.query.filter_by(incident_num=newrow_split[0]).one()
            except:
                incident_num = newrow_split[0]
                category = newrow_split[1]
                description = newrow_split[2]
                if category == "ASSAULT":
                    if "AGGRAVATED" in description:
                        map_category = "Aggravated Assault"
                    else:
                        map_category = "Simple Assault"
                else:
                    if category in map_category_dict:
                        map_category = map_category_dict[category]
                    else:
                        map_category = "Other"
                day_of_week = newrow_split[3]
                date_input = newrow_split[4]
                date = datetime.strptime(date_input, "%m/%d/%Y %H:%M:%S %p")
                time_input = newrow_split[5]
                time = datetime.strptime(time_input,"%H:%M").time()
                district = newrow_split[6]
                address = newrow_split[8]
                x_cord = newrow_split[9]
                y_cord = newrow_split[10]
                
                incident = Crime_Stat(incident_num=incident_num,category=category,description=description,map_category=map_category,
                    day_of_week=day_of_week,date=date,month=month,time=time,hour=hour,address=address,district=district,x_cord=x_cord,
                    y_cord=y_cord)
                db.session.add(incident)

                if i % 1000 == 0:
                    db.session.commit()

    max_date = Crime_Stat.query.order_by(desc(Crime_Stat.date)).first().date
    data_import = Data_Import(max_date=max_date)
    db.session.add(data_import)

    db.session.commit()

    print("finished refreshing")

    flash('Crime stats refreshed')
    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

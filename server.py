from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import Crime_Stat, Victim_Stat, Data_Import, connect_to_db, db
# from seed import load_recent_stats #FIX ME
import json
import decimal
import requests
from sqlalchemy import desc
import csv
from datetime import datetime

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
   
    return render_template("homepage.html")
    
@app.route('/crime')
def get_crime_markers():
    """Make json object containing crime data"""

    start_date = request.args.get("start_date") 
    print start_date
    end_date = request.args.get("end_date")

    if start_date:

        print "start_date has been posted"

        start_date_formatted = datetime.strptime(start_date,"%m/%d/%Y")
        end_date_formatted = datetime.strptime(end_date,"%m/%d/%Y")

        crime_stats = Crime_Stat.query.filter(Crime_Stat.date >= start_date_formatted, Crime_Stat.date <= end_date_formatted).limit(10).all()
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
                              "marker-color": "#fc4353",
                              "marker-size": "large",
                              "marker-symbol": "monument"
                            }
                          }

            marker_object_list.append(marker_object)              

        marker_object_dict["features"] = marker_object_list    

        return jsonify(marker_object_dict)

    else:    

        crime_stats = Crime_Stat.query.limit(10).all()
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
                              "marker-color": "#fc4353",
                              "marker-size": "large",
                              "marker-symbol": "monument"
                            }
                          }

            marker_object_list.append(marker_object)            

        marker_object_dict["features"] = marker_object_list    

        return jsonify(marker_object_dict)

@app.route('/probability')
def get_probability_stats():
    """Get probability stats based on gender and age."""

    age = request.args.get("age") 
    print age
    gender = request.args.get("gender")
    print gender


    victim_stats = Victim_Stat.query.filter_by(age_range=age, gender=gender).all()

    victim_dict = {}

    for victim in victim_stats:
        victim_dict[victim.category] = str(decimal.Decimal(victim.percent))

    print victim_dict

    return jsonify(victim_dict)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

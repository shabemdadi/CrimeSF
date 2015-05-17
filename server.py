from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import Crime_Stat, Victim_Stats, connect_to_db, db
import json
import decimal
import requests
import time
from datetime import datetime, timedelta

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
   
    return render_template("homepage.html") 
    
@app.route('/crime')
def get_crime_stats():

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
                          "title": "Mapbox DC",
                          "description": crime.map_category,
                          "marker-color": "#fc4353",
                          "marker-size": "large",
                          "marker-symbol": "monument"
                        }
                      }

        marker_object_list.append(marker_object)              

    marker_object_dict["features"] = marker_object_list    
    # final_marker_list = """{ "type": "FeatureCollection","features": [""" + marker_list + "]}"

    print jsonify(marker_object_dict)
    return jsonify(marker_object_dict)

def get_recent_crime():

    current_datetime = datetime.now()
    month_ago_date = current_datetime.strftime('%m/%d/%Y')
    month_ago_time = current_datetime.strftime('%H:%M')


    data = requests.get("https://data.sfgov.org/resource/ritf-b9ki.json$$app_token=RvFtAMemRY6per3vRmUEutOfM?date>%sANDtime>%s" % (month_ago_date, month_ago_time)


    

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

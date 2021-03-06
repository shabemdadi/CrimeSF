from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from demo_model import Crime_Stat, Data_Import, Hour_Count, Day_Count, Month_Count, connect_to_db, db
import json
import requests
from sqlalchemy import desc
import csv
from datetime import datetime, timedelta
import time
import ast
import os

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

    start_date = request.args.get("start_date") #start_date and end_date are defined in the event listener in javascript and passed into Flask
    end_date = request.args.get("end_date")

    if start_date:                              #if the user enters in a start_date

        print start_date

        start_date_formatted = datetime.strptime(start_date,"%Y-%m-%d") #reformat start and end dates as date objects
        end_date_formatted = datetime.strptime(end_date,"%Y-%m-%d")
        
        return Crime_Stat.get_features_objects_by_date(start_date_formatted,end_date_formatted) #call class method that will return GeoJSON features

    else:                               # user has not entered in a date, use a default period
        
        end_date = datetime.now()                    
        start_date = end_date - timedelta(days=15)

        print start_date

        return Crime_Stat.get_features_objects_by_date(start_date,end_date)

@app.route('/heat')
def show_heat():
    """Show heatmap"""

    return render_template("heatmap.html")

    
@app.route('/get_heat')
def get_heat_points():
    """Make JSON objects for markers on heatmap."""

    start_date = request.args.get("start_date") #start_date and end_date are defined in the event listener in javascript and passed into Flask
    end_date = request.args.get("end_date")

    if start_date:                              #if the user enters in a start_date

        print start_date
        print end_date

        start_date_formatted = datetime.strptime(start_date,"%Y-%m-%d") #reformat start and end dates as date objects
        end_date_formatted = datetime.strptime(end_date,"%Y-%m-%d")
        
        return Crime_Stat.get_features_objects_by_date(start_date_formatted,end_date_formatted)

    else:                               # user has not entered in a date, use a default period
        
        end_date = datetime.now()                    
        start_date = end_date - timedelta(days=15)

        print start_date

        return Crime_Stat.get_features_objects_by_date(start_date,end_date)

@app.route('/trends')
def show_charts():
    """Show trend line graphs"""

    return render_template("charts.html")


@app.route('/get_hour_stats')
def get_hour_stats():
    """Get hour data to be rendered on charts.js"""

    map_categories = str(request.args.get("map_categories")) #put JS returned into string
    map_categories_list = map_categories.strip("]").strip("[").split(",") #put string into list
    category_list = []

    for category in map_categories_list:    #iterate through the list to strip out quotes and add to a list
        category_stripped = category.strip('"')
        category_list.append(category_stripped)

    if map_categories != "None":    #if there is no checkbox checked JS will return "None" as a string

        return Crime_Stat.get_hour_data_category(category_list) #call class method querying database by hour and provided catory and returns graph variable

    else:

        return Crime_Stat.get_hour_data() #if no categories provided, get all data regardless of category (this is what happens when page first loads)

@app.route('/get_day_stats')
def get_day_stats():
    """Get day data to be rendered on charts.js"""

    map_categories = str(request.args.get("map_categories"))
    map_categories_list = map_categories.strip("]").strip("[").split(",")
    category_list = []

    for category in map_categories_list:
        category_stripped = category.strip('"')
        category_list.append(category_stripped)

    if map_categories != "None":

        return Crime_Stat.get_day_data_category(category_list)

    else:

        return Crime_Stat.get_day_data()

@app.route('/get_month_stats')
def get_month_stats():
    """Get month data to be rendered on charts.js"""

    map_categories = str(request.args.get("map_categories"))
    map_categories_list = map_categories.strip("]").strip("[").split(",")
    category_list = []

    for category in map_categories_list:
        category_stripped = category.strip('"')
        category_list.append(category_stripped)

    if map_categories != "None":

        return Crime_Stat.get_month_data_category(category_list)

    else:

        return Crime_Stat.get_month_data()

@app.route('/journey')
def get_route():
    """Show routing map"""

    return render_template("journey.html")

@app.route('/report')
def show_report_page():
    """Show routing map"""

    return render_template("report.html")

@app.route('/report_crime')
def process_report():
    """Save reported crime to database."""

    time_input = request.args.get("time")
    date_input = request.args.get("date")
    address_input = request.args.get("address")
    description = request.args.get("description")
    map_category = request.args.get("map_category")

    time = datetime.strptime(time_input,"%H:%M").time() #format the time as a datetime object

    date = datetime.strptime(date_input, "%Y-%m-%d")    #format the date as a datetime object
    date_string = datetime.strftime(date,"%Y-%m-%d")    #format date as a string

    #use the Mapbox geocoder API to get the coordinates of the addressed inputted
    geocode = requests.get("http://api.tiles.mapbox.com/v4/geocode/mapbox.places/'%s'.json?access_token=pk.eyJ1Ijoic2hhYmVtZGFkaSIsImEiOiIwckNSMkpvIn0.MeYrWfZexYn1AwdiasXbsg" % address_input)
    geocode_text = geocode.text     #put the response into text
    geocode_json = json.loads(geocode_text) #read in as json

    coordinates = geocode_json["features"][0]["geometry"]["coordinates"]    #this will return the coordinates of the first returned location, sometimes there is more than one, maybe deal with this later

    y_cord = coordinates[0]
    x_cord = coordinates[1]
    address = address_input

    data_source = "citizen"
    day_of_week = datetime.strftime(date,"%A")  #get a string with the day of the week
    month = datetime.strftime(date,"%B")        #get a string with the month
    hour = time.strftime("%H:00")               # get a string with the hour
    incident_id = Crime_Stat.query.order_by(desc(Crime_Stat.incident_id)).first().incident_id + 1

    #see if another user has submitted a report on the same date, at the dame location, at the same hour, and with the same category
    overlap = Crime_Stat.query.filter_by(date=date_string,x_cord=x_cord,y_cord=y_cord,hour=hour,map_category=map_category).all()

    #if so, do not update the database
    if overlap:
        
        return jsonify({"nothing":"nothing"})

    #if not, update the database with the citizen report and call the feature object method on the instance so there will be a marker passed to the map
    else:

        incident = Crime_Stat(incident_id=incident_id,data_source=data_source, description=description,map_category=map_category,day_of_week=day_of_week,date=date,
            month=month,time=time,hour=hour,address=address,x_cord=x_cord,y_cord=y_cord)
        
        db.session.add(incident)

        db.session.commit()

        feature_object = incident.make_feature_object()

        return jsonify(feature_object)

@app.route('/get_recent')  #This will happen when the user clicks on the "Get Recent Stats" button, it will update our database and update our counts tables with the same function used in our seed file
def get_recent_stats():
    """Check API to see if there are new crime stats, if so, import into database."""

    print "refresh started at %s" % datetime.now()

    map_category_dict = {'LARCENY/THEFT':'Personal Theft/Larceny',
                 'BURGLARY':'Robbery',
                 'SEX OFFENSES, FORCIBLE':'Rape/Sexual Assault',
                 'VEHICLE THEFT':'Personal Theft/Larceny',
                 'ROBBERY':'Personal Theft/Larceny',
                 'STOLEN PROPERTY':'Personal Theft/Larceny',
                 'SEX OFFENSES, NON FORCIBLE':'Rape/Sexual Assault'
                 }

    recent_import_date = Data_Import.query.order_by(desc(Data_Import.max_date)).first().max_date

    print recent_import_date

    recent_import_date_formatted = recent_import_date.strftime('%Y-%m-%dT%H:%M:%S')

    data = requests.get("https://data.sfgov.org/resource/gxxq-x39z.json?$WHERE=date>='%s'&$$app_token=RvFtAMemRY6per3vRmUEutOfM" % recent_import_date_formatted)

    data_text = data.text

    data_json = json.loads(data_text)

    for i, row in enumerate(data_json):
        if i > 0:
            try:
                overlap = Crime_Stat.query.filter_by(incident_num=row["incidntnum"],category=row["category"]).one()
            except:
                incident_num = row["incidntnum"]
                category = row["category"]
                data_source = "official"
                description = row["descript"]
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
                day_of_week = row["dayofweek"]
                date_input = row["date"]
                date = datetime.strptime(date_input, "%Y-%m-%dT%H:%M:%S")
                month = datetime.strftime(date,"%B")
                time_input = row["time"]
                time = datetime.strptime(time_input,"%H:%M").time()
                hour = time.strftime("%H:00")
                district = row["pddistrict"]
                address = row["address"]
                x_cord = row["location"]["latitude"]
                y_cord = row["location"]["longitude"]
                incident_id = Crime_Stat.query.order_by(desc(Crime_Stat.incident_id)).first().incident_id + 1
                
                incident = Crime_Stat(incident_id=incident_id,incident_num=incident_num,data_source=data_source,category=category,description=description,map_category=map_category,
                    day_of_week=day_of_week,date=date,month=month,time=time,hour=hour,address=address,district=district,x_cord=x_cord,
                    y_cord=y_cord)
                db.session.add(incident)

                if i % 1000 == 0:
                    db.session.commit()

    max_date = Crime_Stat.query.filter(Crime_Stat.data_source != "citizen").order_by(desc(Crime_Stat.date)).first().date
    import_id = Data_Import.query.order_by(desc(Data_Import.import_id)).first().import_id + 1
    data_import = Data_Import(import_id=import_id,max_date=max_date)
    db.session.add(data_import)

    db.session.commit()

    print "finished refreshing at %s" % datetime.now()
    print "refreshing counts at %s" % datetime.now()

    Hour_Count.query.delete()
    Day_Count.query.delete()
    Month_Count.query.delete()

    map_category_list = ['Personal Theft/Larceny','Robbery', 'Rape/Sexual Assault','Aggravated Assault','Simple Assault','Other']
    hours_list = ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00",
                  "16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00"]
    day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    month_list = ["January","February","March","April","May","June","July","August","September","October","November","December"]

    for hour in hours_list:
        for category in map_category_list:
            count = Crime_Stat.query.filter_by(hour=hour,map_category=category).count()
            hour_stat = Hour_Count(hour=hour,map_category=category,count=count)
            db.session.add(hour_stat)

        count_all = Crime_Stat.query.filter_by(hour=hour).count() 
        hour_stat = Hour_Count(hour=hour,map_category="all",count=count_all)
        db.session.add(hour_stat)

    db.session.commit()

    for day in day_list:
        for category in map_category_list:
            count = Crime_Stat.query.filter_by(day_of_week=day,map_category=category).count()
            day_stat = Day_Count(day=day,map_category=category,count=count)
            db.session.add(day_stat)

        count_all = Crime_Stat.query.filter_by(day_of_week=day).count() 
        day_stat = Day_Count(day=day,map_category="all",count=count_all)
        db.session.add(day_stat)

    db.session.commit()

    for month in month_list:
        for category in map_category_list:
            count = Crime_Stat.query.filter_by(month=month,map_category=category).count()
            month_stat = Month_Count(month=month,map_category=category,count=count)
            db.session.add(month_stat)

        count_all = Crime_Stat.query.filter_by(month=month).count() 
        month_stat = Month_Count(month=month,map_category="all",count=count_all)
        db.session.add(month_stat)

    db.session.commit()

    print "finished refreshing counts at %s" % datetime.now()

    flash('Crime stats refreshed')
    return redirect(request.referrer)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    # app.debug = True

    connect_to_db(app)

    secret_key = os.environ.get("FLASK_SECRET_KEY", "ABC")

    app.config['secret_key'] = secret_key

    DEBUG = "NO_DEBUG" not in os.environ

    PORT = int(os.environ.get("PORT", 5000))

    app.run(debug=DEBUG, host="0.0.0.0", port=PORT)


    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False #this is so the toolbar does not interrupt redirects

    # app.run()
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import Crime_Stat, Data_Import, Hour_Count, Day_Count, Month_Count, connect_to_db, db
import json
import requests
from sqlalchemy import desc
import csv
from datetime import datetime, timedelta
import time
import ast

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

    # time.sleep(30)

    start_date = request.args.get("start_date") #start_date and end_date are defined in the event listener in javascript and passed into Flask
    print start_date
    end_date = request.args.get("end_date")

    if start_date:                              #if the user enters in a start_date

        print "start_date has been posted"

        start_date_formatted = datetime.strptime(start_date,"%Y-%m-%d") #reformat start and end dates as date objects
        end_date_formatted = datetime.strptime(end_date,"%Y-%m-%d")
        
        return Crime_Stat.get_features_objects_by_date(start_date_formatted,end_date_formatted) #call class method that will return GeoJSON features

    else:                               # user has not entered in a date, use a default period of 45 days ago
        
        end_date = datetime.now()                    
        start_date = end_date - timedelta(days=30)

        print start_date

        return Crime_Stat.get_features_objects_by_date(start_date,end_date)

@app.route('/heat')
def show_heat():
    """Show heatmap"""

    return render_template("heatmap.html")

    
@app.route('/get_heat')
def get_heat_points():
    """Make JSON objects for markers on heatmap."""

    # time.sleep(30)

    start_date = request.args.get("start_date") #start_date and end_date are defined in the event listener in javascript and passed into Flask
    print start_date
    end_date = request.args.get("end_date")

    if start_date:                              #if the user enters in a start_date

        print "start_date has been posted"

        start_date_formatted = datetime.strptime(start_date,"%Y-%m-%d") #reformat start and end dates as date objects
        end_date_formatted = datetime.strptime(end_date,"%Y-%m-%d")
        
        return Crime_Stat.get_features_objects_by_date(start_date_formatted,end_date_formatted)

    else:                               # user has not entered in a date, use a default period of 45 days ago
        
        end_date = datetime.now()                    
        start_date = end_date - timedelta(days=30)

        print start_date

        return Crime_Stat.get_features_objects_by_date(start_date,end_date)

@app.route('/trends')
def show_charts():
    """Show trend line graphs"""

    date_now = datetime.now()                                       #Show current date and time
    date_formatted = datetime.strftime(date_now,"%A, %B %d, %Y")
    time_formatted = datetime.strftime(date_now, "%H:%M")

    return render_template("charts.html",date=date_formatted,time=time_formatted)


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

        print "in map_categories"

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

        print "in map_categories"

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

        print "in map_categories"

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

@app.route('/report_crime', methods=["POST"])
def process_report():
    """Save reported crime to database."""

    time = request.form.get("time")
    print time
    date = request.form.get("date")
    print date
    address = request.form.get("address")
    print address
    description = request.form.get("description")
    print description
    map_category = request.form.get("category")
    print map_category

    # incident_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # incident_num = db.Column(db.String(60), nullable=False) #want this to be nullable
    # category = db.Column(db.String(60), nullable=False)     #want this to be nullable
    # map_category = db.Column(db.String(60), nullable=False)
    # description = db.Column(db.String(200), nullable=False)
    # day_of_week = db.Column(db.String(10), nullable=False)
    # date = db.Column(db.Date, nullable=False)
    # month = db.Column(db.String(10), nullable=False)
    # time = db.Column(db.Time, nullable=False)
    # hour = db.Column(db.String(10), nullable=False)
    # district = db.Column(db.String(60), nullable=False) #want this to be nullable
    # address = db.Column(db.String(60), nullable=False)
    # x_cord = db.Column(db.Numeric, nullable=False)
    # y_cord = db.Column(db.Numeric, nullable=False)

    # incident = Crime_Stat(incident_num=incident_num,category=category,description=description,map_category=map_category,
    #                 day_of_week=day_of_week,date=date,month=month,time=time,hour=hour,address=address,district=district,x_cord=x_cord,
    #                 y_cord=y_cord)
    
    # db.session.add(incident)

    # db.session.commit()

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
                overlap = Crime_Stat.query.filter_by(incident_num=row["incidntnum"]).one()
            except:
                incident_num = row["incidntnum"]
                category = row["category"]
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

    current_path = request.args.get("current_path")
    print current_path
    flash('Crime stats refreshed')
    return redirect(current_path)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

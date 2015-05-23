from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import Crime_Stat, Victim_Stat, Data_Import, connect_to_db, db
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

    start_date = request.form.get("start_date") 
    print start_date
    end_date = request.form.get("end_date")

    if start_date:

        print "start_date has been posted"

        start_date_formatted = datetime.strptime(start_date,"%Y-%m-%d")
        end_date_formatted = datetime.strptime(end_date,"%Y-%m-%d")

        crime_stats = Crime_Stat.query.filter(Crime_Stat.date >= start_date_formatted, Crime_Stat.date <= end_date_formatted).limit(100).all()
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
                              "marker-color": '#FF0000',
                              "marker-size": "small",
                              "marker-symbol": "marker"
                            }
                          }

            marker_object_list.append(marker_object)              

        marker_object_dict["features"] = marker_object_list    

        return jsonify(marker_object_dict)

    else: 

        marker_color_dict = {'Personal Theft/Larceny':'#FF0000',
                                'Robbery':'#0000FF',
                                'Rape/Sexual Assault':'#008000',
                                'Aggravated Assault':'#FFA500',
                                'Simple Assault':'#6600CC',
                                'Other':'#669999',
                            }

        
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

@app.route('/heat', methods=["POST","GET"])
def show_heat():
    """Show heatmap"""

    return render_template("heatmap.html")

    
@app.route('/get_heat', methods=["POST","GET"])
def get_heat_points():
    """Make JSON objects for markers on heatmap."""

    start_date = request.args.get("start_date") 
    print start_date
    end_date = request.args.get("end_date")

    if start_date:

        print "start_date has been posted"

        start_date_formatted = datetime.strptime(start_date,"%Y-%m-%d")
        end_date_formatted = datetime.strptime(end_date,"%Y-%m-%d")

        crime_stats = Crime_Stat.query.filter(Crime_Stat.date >= start_date_formatted, Crime_Stat.date <= end_date_formatted).limit(200).all()
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
                              "marker-color": '#FF0000',
                              "marker-size": "small",
                              "marker-symbol": "marker"
                            }
                          }

            marker_object_list.append(marker_object)              

        marker_object_dict["features"] = marker_object_list    

        return jsonify(marker_object_dict)

    else:    

        crime_stats = Crime_Stat.query.limit(200).all()
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

@app.route('/trends')
def get_chart_data():
    """Get data to be rendered on charts.js"""

    crime_stats = Crime_Stat.query.limit(10).all()
    data_point_list = []
    label_list = []

    for crime in crime_stats:
        time = crime.time

    data = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
        {
            label: "My First dataset",
            fillColor: "rgba(220,220,220,0.2)",
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: [65, 59, 80, 81, 56, 55, 40]
        }
    ]
};

    render_template("charts.html")

@app.route('/get_recent')
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
                
                incident = Crime_Stat(incident_num=incident_num,category=category,address=address,description=description,map_category=map_category,day_of_week=day_of_week,
                    date=date,time=time,district=district,x_cord=x_cord,y_cord=y_cord)
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

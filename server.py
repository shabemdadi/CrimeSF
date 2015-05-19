from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import Crime_Stat, Victim_Stat, Data_Import, connect_to_db, db
import json
import decimal
import requests
from sqlalchemy import desc
import csv

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    # map_category_dict = {'LARCENY/THEFT':'Personal Theft/Larceny',
    #                  'BURGLARY':'Robbery',
    #                  'SEX OFFENSES, FORCIBLE':'Rape/Sexual Assault',
    #                  'VEHICLE THEFT':'Personal Theft/Larceny',
    #                  'ROBBERY':'Personal Theft/Larceny',
    #                  'ARSON':'Personal Theft/Larceny',
    #                  'STOLEN PROPERTY':'Personal Theft/Larceny',
    #                  'SEX OFFENSES, NON FORCIBLE':'Rape/Sexual Assault'
    #                  }

    # recent_import_date = Data_Import.query.order_by(desc(Data_Import.max_date)).first().max_date

    # recent_import_date_formatted = recent_import_date.strftime('%Y-%m-%dT%H:%M:%S')

    # data = requests.get("https://data.sfgov.org/resource/gxxq-x39z.csv?$WHERE=date>='%s'&$$app_token=RvFtAMemRY6per3vRmUEutOfM" % recent_import_date_formatted)

    # data_text = data.text

    # reader = csv.reader(data_text.splitlines(), delimiter='\t')

    # for i, row in enumerate(reader):
    #     if i > 0:
    #         try:
    #             Crime_Stat.query.filter_by(incident_num=row[0]).first()
    #         except:
    #                 incident_num = row[0]
    #                 category = row[1]
    #                 description = row[2]
    #                 if category == "ASSAULT":
    #                     if "AGGRAVATED" in description:
    #                         map_category = "Aggravated assault"
    #                     else:
    #                         map_category = "Simple assault"
    #                 else:
    #                     if category in map_category_dict:
    #                         map_category = map_category_dict[category]
    #                     else:
    #                         map_category = "Other"
    #                 day_of_week = row[3]
    #                 date_input = row[4]
    #                 date = datetime.strptime(date_input, "%m/%d/%Y %H:%M")
    #                 time_input = row[5]
    #                 time = datetime.strptime(time_input,"%H:%M").time()
    #                 district = row[6]
    #                 address = row[8]
    #                 x_cord = row[9]
    #                 y_cord = row[10]
                    
    #                 incident = Crime_Stat(incident_num=incident_num,category=category,address=address,description=description,map_category=map_category,day_of_week=day_of_week,
    #                     date=date,time=time,district=district,x_cord=x_cord,y_cord=y_cord)
    #                 db.session.add(incident)
    #                 if i % 1000 == 0:
    #                     db.session.commit()

    #     max_date = Crime_Stat.query.order_by(desc(Crime_Stat.date)).first().date
    #     data_import = Data_Import(max_date=max_date)
    #     db.session.add(data_import)

    #     db.session.commit()
   
    return render_template("homepage.html") 
    
@app.route('/crime')
def get_crime_stats():
    """Update crime stats database with API call and make json object containing crime data"""

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

    print jsonify(marker_object_dict)
    return jsonify(marker_object_dict)
    

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

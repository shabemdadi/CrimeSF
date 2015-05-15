from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import Crime_Stat,connect_to_db, db
import json
import decimal

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
   
    return render_template("homepage2.html") 
    
@app.route('/crime')
def get_crime_stats():

    crime_stats = Crime_Stat.query.limit(10).all()
    crime_dict = {}
    
    for crime in crime_stats:           # need to add in address
        crime_dict[crime.incident_id] = {}
        crime_dict[crime.incident_id]['lat'] = str(decimal.Decimal(crime.x_cord))
        crime_dict[crime.incident_id]['long'] = str(decimal.Decimal(crime.y_cord))
        crime_dict[crime.incident_id]['id'] = crime.incident_id
        
    print jsonify(crime_dict)
    return jsonify(crime_dict)
                
    
@app.route('/users')
def get_user_profile():
    """Displays form where user can input info and routes to be added to their profile"""
    
    return render_template("user_form.html")

@app.route("/user_profile", methods = ["POST"])
def show_user_profile():
    """Gets user input information and display user profile"""
    
    return render_template("user_profile.html")
    
    

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

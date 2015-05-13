from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html") 
    
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

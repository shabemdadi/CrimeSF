"""Models and database functions for final project."""

from flask_sqlalchemy import SQLAlchemy
import decimal

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Crime_Stat(db.Model):

    """Table of crime statistics."""

    __tablename__ = "crime_stats"
    
    incident_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    incident_num = db.Column(db.String(60), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    map_category = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    district = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    x_cord = db.Column(db.Numeric, nullable=False)
    y_cord = db.Column(db.Numeric, nullable=False)
    
    
class Victim_Stat(db.Model):
    """Table of victim data"""
    
    __tablename__ = "victim_stats"
    
    victim_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    age_range = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    percent = db.Column(db.Numeric, nullable=False)

class Data_Import(db.Model):
    """Table showing info on last crime statictics import"""

    __tablename__ = "data_imports"

    import_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    max_date = db.Column(db.Date, nullable=False)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crimes.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    
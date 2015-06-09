"""Models and database functions for final project."""

from flask_sqlalchemy import SQLAlchemy
import decimal
from datetime import datetime
from flask import jsonify
from time import time

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
    incident_num = db.Column(db.String(60), nullable=False) #want this to be nullable for citizen report
    category = db.Column(db.String(60), nullable=False)     #want this to be nullable for citizen report
    map_category = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    month = db.Column(db.String(10), nullable=False)
    time = db.Column(db.Time, nullable=False)
    hour = db.Column(db.String(10), nullable=False)
    district = db.Column(db.String(60), nullable=False) #want this to be nullable for citizen report
    address = db.Column(db.String(60), nullable=False)
    x_cord = db.Column(db.Numeric, nullable=False)
    y_cord = db.Column(db.Numeric, nullable=False)

    def make_feature_object(self):
        """Make GeoJSON feature object"""

        date_formatted = datetime.strftime(self.date,"%m/%d/%Y") #format time and date as strings to use in feature objects
        time_formatted = self.time.strftime("%I:%M %p")

        marker_color_dict = {'Personal Theft/Larceny':'#FF0000', #This dictionary will link the type of crime to the color marker it will be assigned    
                                'Robbery':'#0000FF',
                                'Rape/Sexual Assault':'#008000',
                                'Aggravated Assault':'#FFA500',
                                'Simple Assault':'#6600CC',
                                'Other':'#669999',
                            }

        feature_object = {
                                "type": "Feature",
                                "geometry": {
                                  "type": "Point",
                                  "coordinates": [str(decimal.Decimal(self.y_cord)), str(decimal.Decimal(self.x_cord))] #deal with decimal from database
                                },
                                "properties": {
                                  "title": self.map_category,
                                  "description": str(self.description).title(), #put description in string and called title capitalization on it
                                  "date": date_formatted,
                                  "time":time_formatted,
                                  "address":self.address,
                                  "marker-color": marker_color_dict[self.map_category], #use marker color dictionary to assign marker colors based on type of crime
                                  "marker-size": "small",
                                  "marker-symbol": "marker"
                                }
                              }

        return feature_object

    @classmethod
    def get_features_objects_by_date(cls,start_date,end_date):
        """Query table and then make feature objects on each instance to be sent to map"""

        crime_stats = cls.query.filter(cls.date >= start_date, cls.date <= end_date).all() #create query object of rows that fall in time range

        print len(crime_stats)
        
        marker_object_dict = { "type": "FeatureCollection"}
        marker_object_list = []

        for crime in crime_stats:                               #iterate over query object calling the feature object class method on each
            marker_object = crime.make_feature_object()

            marker_object_list.append(marker_object)            #append each feature object to a list  

        marker_object_dict["features"] = marker_object_list     #add list of feature objects to the value of a key

        return jsonify(marker_object_dict)

    @classmethod
    def get_hour_data(cls):
        """Create chart variable with labels and datapoints for hour trend graph."""

        label_list = ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00",
                  "16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00"]
        data_point_list = []

        for hour in label_list: #iterate over each hour, and query the database to find the count of crimes happening in each hour. The count will be the datapoint for that hour.
            count_crimes = Hour_Count.query.filter_by(hour=hour,map_category="all").one().count
            data_point_list.append(count_crimes)

        data = {"labels": label_list, "datasets": [   #this is the data variable that will be passed into the graph
            {"label": "My First dataset",
            "fillColor": "rgba(151,187,205,0.2)",
            "strokeColor": "rgba(151,187,205,1)",
            "pointColor": "rgba(151,187,205,1)",
            "pointStrokeColor": "#fff",
            "pointHighlightFill": "#fff",
            "pointHighlightStroke": "rgba(151,187,205,1)",
            "data": data_point_list}]
            }

        return jsonify(data)


    @classmethod
    def get_day_data(cls):
        """Create chart variable with labels and datapoints for day trend graph."""

        data_point_list = []
        label_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

        for day in label_list: #iterate over each day, and query the database to find the count of crimes happening on each day. The count will be the datapoint for that day.
            count_crimes = Day_Count.query.filter_by(day=day,map_category="all").one().count
            data_point_list.append(count_crimes)

        data = {"labels": label_list, "datasets": [ #this is the data variable that will be passed into the graph
            {"label": "My First dataset",
            "fillColor": "rgba(151,187,205,0.2)",
            "strokeColor": "rgba(151,187,205,1)",
            "pointColor": "rgba(151,187,205,1)",
            "pointStrokeColor": "#fff",
            "pointHighlightFill": "#fff",
            "pointHighlightStroke": "rgba(151,187,205,1)",
            "data": data_point_list}]
            }

        return jsonify(data)

    @classmethod
    def get_month_data(cls):
        """Create chart variable with labels and datapoints for month trend graph."""

        data_point_list = []
        label_list = ["January","February","March","April","May","June","July","August","September","October","November","December"]

        for month in label_list: #iterate over each month, and query the database to find the count of crimes happening in each month. The count will be the datapoint for that month.
            count_crimes = Month_Count.query.filter_by(month=month,map_category="all").one().count
            data_point_list.append(count_crimes)

        data = {"labels": label_list, "datasets": [  #this is the data variable that will be passed into the graph
            {"label": "My First dataset",
            "fillColor": "rgba(151,187,205,0.2)",
            "strokeColor": "rgba(151,187,205,1)",
            "pointColor": "rgba(151,187,205,1)",
            "pointStrokeColor": "#fff",
            "pointHighlightFill": "#fff",
            "pointHighlightStroke": "rgba(151,187,205,1)",
            "data": data_point_list}]
            }
 
        return jsonify(data)

    @classmethod
    def get_hour_data_category(cls,map_categories):
        """Create chart variable with labels and datapoints for hour trend graph, taking into account map_category."""

        label_list = ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00",
                  "16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00"]
        data_point_list = []

        for hour in label_list:  #iterate over each hour, and query the database to find the count of crimes happening in each hour for the categories checked in checkboxes. The count will be the datapoint for that hour.
            count_crimes = Hour_Count.query.filter(Hour_Count.hour==hour, Hour_Count.map_category.in_(map_categories)).all()
            total_count = sum([count.count for count in count_crimes])
            data_point_list.append(total_count)

        data = {"labels": label_list, "datasets": [   #this is the data variable that will be passed into the graph
            {"label": "My First dataset",
            "fillColor": "rgba(151,187,205,0.2)",
            "strokeColor": "rgba(151,187,205,1)",
            "pointColor": "rgba(151,187,205,1)",
            "pointStrokeColor": "#fff",
            "pointHighlightFill": "#fff",
            "pointHighlightStroke": "rgba(151,187,205,1)",
            "data": data_point_list}]
            }

        return jsonify(data)

    @classmethod
    def get_day_data_category(cls,map_categories):
        """Create chart variable with labels and datapoints for day trend graph, taking into account map_category."""

        label_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        data_point_list = []

        for day in label_list: #iterate over each day, and query the database to find the count of crimes happening on each day using the catagories checked in checkboxes. The count will be the datapoint for that day.
            count_crimes = Day_Count.query.filter(Day_Count.day==day, Day_Count.map_category.in_(map_categories)).all()
            total_count = sum([count.count for count in count_crimes])

            data_point_list.append(total_count)

        data = {"labels": label_list, "datasets": [   #this is the data variable that will be passed into the graph
            {"label": "My First dataset",
            "fillColor": "rgba(151,187,205,0.2)",
            "strokeColor": "rgba(151,187,205,1)",
            "pointColor": "rgba(151,187,205,1)",
            "pointStrokeColor": "#fff",
            "pointHighlightFill": "#fff",
            "pointHighlightStroke": "rgba(151,187,205,1)",
            "data": data_point_list}]
            }

        return jsonify(data)

    @classmethod
    def get_month_data_category(cls,map_categories):
        """Create chart variable with labels and datapoints for month trend graph, taking into account map_category."""

        label_list = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        data_point_list = []

        for month in label_list:    #iterate over each month, and query the database to find the count of crimes happening in each month and for crime catagories denoted by checkboxes. The count will be the datapoint for that month.
            count_crimes = Month_Count.query.filter(Month_Count.month==month, Month_Count.map_category.in_(map_categories)).all()
            total_count = sum([count.count for count in count_crimes])
            data_point_list.append(total_count)

        data = {"labels": label_list, "datasets": [   #this is the data variable that will be passed into the graph
            {"label": "My First dataset",
            "fillColor": "rgba(151,187,205,0.2)",
            "strokeColor": "rgba(151,187,205,1)",
            "pointColor": "rgba(151,187,205,1)",
            "pointStrokeColor": "#fff",
            "pointHighlightFill": "#fff",
            "pointHighlightStroke": "rgba(151,187,205,1)",
            "data": data_point_list}]
            }

        return jsonify(data)

class Hour_Count(db.Model):
    """Table showing counts of crime by hour and crime category."""

    __tablename__ = "hour_counts"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hour = db.Column(db.String(10),nullable=False)
    map_category = db.Column(db.String(60), nullable=False)
    count = db.Column(db.Integer,nullable=False)

class Day_Count(db.Model):
    """Table showing counts of crime by day and crime category."""

    __tablename__ = "day_counts"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    day = db.Column(db.String(10),nullable=False)
    map_category = db.Column(db.String(60), nullable=False)
    count = db.Column(db.Integer,nullable=False)

class Month_Count(db.Model):
    """Table showing counts of crime by month and crime category."""

    __tablename__ = "month_counts"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    month = db.Column(db.String(10),nullable=False)
    map_category = db.Column(db.String(60), nullable=False)
    count = db.Column(db.Integer,nullable=False)

class Data_Import(db.Model):
    """Table showing info on last crime statistics import"""

    __tablename__ = "data_imports"

    import_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    max_date = db.Column(db.Date, nullable=False)       #this will be the date of the most recent imported crime statistic

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
    
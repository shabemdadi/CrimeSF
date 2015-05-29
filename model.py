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
    incident_num = db.Column(db.String(60), nullable=False)
    category = db.Column(db.String(60), nullable=False)
    map_category = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    day_of_week = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False)
    month = db.Column(db.String(10), nullable=False)
    time = db.Column(db.Time, nullable=False)
    hour = db.Column(db.String(10), nullable=False)
    district = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(60), nullable=False)
    x_cord = db.Column(db.Numeric, nullable=False)
    y_cord = db.Column(db.Numeric, nullable=False)

    def make_feature_object(self):
        """Make feature object"""

        date_formatted = datetime.strftime(self.date,"%m/%d/%Y")
        time_formatted = self.time.strftime("%I:%M %p")

        marker_color_dict = {'Personal Theft/Larceny':'#FF0000',    #This dictionary will link the type of crime to the color marker it will be assigned    
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
                                  "coordinates": [str(decimal.Decimal(self.x_cord)), str(decimal.Decimal(self.y_cord))] #FIX ME
                                },
                                "properties": {
                                  "title": self.map_category,
                                  "description": self.description,
                                  "date": date_formatted,
                                  "time":time_formatted,
                                  "address":self.address,
                                  "marker-color": marker_color_dict[self.map_category],
                                  "marker-size": "small",
                                  "marker-symbol": "marker"
                                }
                              }

        return feature_object

    @classmethod
    def get_features_objects_by_date(cls,start_date,end_date):
        """Query table and then make feature objects on each instance to be sent to map"""

        print "get feature objects by date"
        print time()
        crime_stats = cls.query.filter(cls.date >= start_date, cls.date <= end_date).all() 
        print len(crime_stats)
        # crime_stats = cls.query.all(
        print time()

        marker_object_dict = { "type": "FeatureCollection"}
        marker_object_list = []

        print "finished querying"

        for crime in crime_stats:
            marker_object = crime.make_feature_object()

            marker_object_list.append(marker_object)              

        print time()
        marker_object_dict["features"] = marker_object_list    

        return jsonify(marker_object_dict)

    @classmethod
    def get_features_objects_by_date_category(cls,start_date,end_date,map_category):
        """Query table and then make feature objects on each instance to be sent to map"""

        print "get feature objects by date"
        print time()
        crime_stats = cls.query.filter(cls.date >= start_date, cls.date <= end_date, cls.map_category.in_(map_category)).all() 
        print len(crime_stats)
        # crime_stats = cls.query.all(
        print time()

        marker_object_dict = { "type": "FeatureCollection"}
        marker_object_list = []

        print "finished querying"

        for crime in crime_stats:
            marker_object = crime.make_feature_object()

            marker_object_list.append(marker_object)              

        print time()
        marker_object_dict["features"] = marker_object_list    

        return jsonify(marker_object_dict)

    @classmethod
    def get_hour_data(cls):
        """Create chart variable with labels and datapoints for hour trend graph."""

        label_list = ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00",
                  "16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00"]
        data_point_list = []

        for hour in label_list:       #iterate over each hour, and query the database to find the count of crimes happening in each hour. The count will be the datapoint for that hour.
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

        for day in label_list:       #iterate over each hour, and query the database to find the count of crimes happening in each hour. The count will be the datapoint for that hour.
            count_crimes = Day_Count.query.filter_by(day=day,map_category="all").one().count
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
    def get_month_data(cls):
        """Create chart variable with labels and datapoints for month trend graph."""

        data_point_list = []
        label_list = ["January","February","March","April","May","June","July","August","September","October","November","December"]

        for month in label_list:       #iterate over each hour, and query the database to find the count of crimes happening in each hour. The count will be the datapoint for that hour.
            count_crimes = Month_Count.query.filter_by(month=month,map_category="all").one().count
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
    def get_hour_data_category(cls,map_categories):
        """Create chart variable with labels and datapoints for hour trend graph, taking into account map_category."""

        label_list = ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00",
                  "16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00"]
        data_point_list = []

        print "in hour class method"
        print map_categories
        print type(map_categories)

        for hour in label_list:       #iterate over each hour, and query the database to find the count of crimes happening in each hour. The count will be the datapoint for that hour.
            count_crimes = Hour_Count.query.filter(Hour_Count.hour==hour, Hour_Count.map_category.in_(map_categories)).all()
            total_count = sum([count.count for count in count_crimes])
            # total_count = 0
            # for count in count_crimes:
            #     total_count = total_count + count.count
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
    """Table showing counts of crime by hour."""

    __tablename__ = "hour_counts"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    hour = db.Column(db.String(10),nullable=False)
    map_category = db.Column(db.String(60), nullable=False)
    count = db.Column(db.Integer,nullable=False)

class Day_Count(db.Model):
    """Table showing counts of crime by hour."""

    __tablename__ = "day_counts"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    day = db.Column(db.String(10),nullable=False)
    map_category = db.Column(db.String(60), nullable=False)
    count = db.Column(db.Integer,nullable=False)

class Month_Count(db.Model):
    """Table showing counts of crime by hour."""

    __tablename__ = "month_counts"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    month = db.Column(db.String(10),nullable=False)
    map_category = db.Column(db.String(60), nullable=False)
    count = db.Column(db.Integer,nullable=False)

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
    
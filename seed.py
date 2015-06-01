"""Utility file to seed crime statistics and victim data"""

from model import Crime_Stat, Data_Import, Hour_Count, Day_Count, Month_Count, connect_to_db, db
from server import app
import csv
from datetime import datetime
from sqlalchemy import desc
import requests
import json


def load_crime_stats():
    """Load crime statistics from CSV file into database"""
    
    # variables in this dataset: 'IncidntNum','Category','Descript','DayOfWeek','Date','Time','PdDistrict','Resolution','Address','X','Y','Location'


    map_category_dict = {'LARCENY/THEFT':'Personal Theft/Larceny',          # Make dictionary linking crime categories from data to catgories on map
                         'BURGLARY':'Robbery',
                         'SEX OFFENSES, FORCIBLE':'Rape/Sexual Assault',
                         'VEHICLE THEFT':'Personal Theft/Larceny',
                         'ROBBERY':'Personal Theft/Larceny',
                         'STOLEN PROPERTY':'Personal Theft/Larceny',
                         'SEX OFFENSES, NON FORCIBLE':'Rape/Sexual Assault'
                         }

    with open('Data\Map__Crime_Incidents_-_from_1_Jan_2003.csv', 'rb') as f:    #read in CSV datafile
        reader = csv.reader(f)
    
        for i, row in enumerate(reader):                          #iterate through CSV datafile, designating database variables to save
            if i > 0:
                incident_num = row[0]
                category = row[1]
                description = row[2]
                if category == "ASSAULT":                          #use description field in CSV datafile to determine if aggravated or simple assault
                    if "AGGRAVATED" in description:
                        map_category = "Aggravated Assault"
                    else:
                        map_category = "Simple Assault"
                else:
                    if category in map_category_dict:
                        map_category = map_category_dict[category]
                    else:                                       #designate everything else as "Other"
                        map_category = "Other"
                day_of_week = row[3]
                date_input = row[4]
                date = datetime.strptime(date_input, "%m/%d/%Y %H:%M:%S %p")
                month = datetime.strftime(date,"%B")
                time_input = row[5]
                time = datetime.strptime(time_input,"%H:%M").time()
                hour = time.strftime("%H:00")
                district = row[6]
                address = row[8]
                x_cord = row[9]
                y_cord = row[10]
                
                incident = Crime_Stat(incident_num=incident_num,category=category,description=description,map_category=map_category,    #make an instance of the Crime_Stat class
                    day_of_week=day_of_week,date=date,month=month,time=time,hour=hour,address=address,district=district,x_cord=x_cord,
                    y_cord=y_cord)
                db.session.add(incident)    # add the instance to the database

                if i % 1000 == 0:           # commit every 1000 rows to deal with memory issues
                    db.session.commit()

        max_date = Crime_Stat.query.order_by(desc(Crime_Stat.date)).first().date #find the maximum date represented in the crime stats database
        data_import = Data_Import(max_date=max_date)                             #save this max date to the date_import table   
        db.session.add(data_import)

        db.session.commit()

def load_recent_stats():
    """Check API to see if there are new crime stats, if so, import into database."""

    map_category_dict = {'LARCENY/THEFT':'Personal Theft/Larceny', #dictionary linking crime categories from data to categories I will show in my map
                 'BURGLARY':'Robbery',
                 'SEX OFFENSES, FORCIBLE':'Rape/Sexual Assault',
                 'VEHICLE THEFT':'Personal Theft/Larceny',
                 'ROBBERY':'Personal Theft/Larceny',
                 'STOLEN PROPERTY':'Personal Theft/Larceny',
                 'SEX OFFENSES, NON FORCIBLE':'Rape/Sexual Assault'
                 }

    recent_import_date = Data_Import.query.order_by(desc(Data_Import.max_date)).first().max_date #get the most recent date in the data_import table

    recent_import_date_formatted = recent_import_date.strftime('%Y-%m-%dT%H:%M:%S') #format date to be put into API call

    data = requests.get("https://data.sfgov.org/resource/gxxq-x39z.json?$WHERE=date>='%s'&$$app_token=RvFtAMemRY6per3vRmUEutOfM" % recent_import_date_formatted)

    data_text = data.text #put JSON into text

    data_json = json.loads(data_text) #put JSON into JSON dict

    for i, row in enumerate(data_json): #iterate over JSON dict, first checking that incident num is not present, and add to databse if not present
        if i > 0:
            try:
                overlap = Crime_Stat.query.filter_by(incident_num=row["incidntnum"]).one()
            except:
                incident_num = row["incidntnum"]
                category = row["category"]
                description = row["descript"]
                if category == "ASSAULT":           #use data description to define if crime is simple or aggravated
                    if "AGGRAVATED" in description:
                        map_category = "Aggravated Assault"
                    else:
                        map_category = "Simple Assault"
                else:
                    if category in map_category_dict:
                        map_category = map_category_dict[category]
                    else:
                        map_category = "Other"  #if data category not in dictionary, assign it other
                day_of_week = row["dayofweek"]
                date_input = row["date"]
                date = datetime.strptime(date_input, "%Y-%m-%dT%H:%M:%S")   #make date a datetime object to be put into database
                month = datetime.strftime(date,"%B")                        #make a string of a month to be put into database
                time_input = row["time"]
                time = datetime.strptime(time_input,"%H:%M").time()         #make time a datetime object to be put into database
                hour = time.strftime("%H:00")                               #make a string of an hour to be put into the database
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

    max_date = Crime_Stat.query.order_by(desc(Crime_Stat.date)).first().date #find the max date in the crime_stats table
    data_import = Data_Import(max_date=max_date)                             #add the max date to the data_import table
    db.session.add(data_import)

    db.session.commit()

def load_crime_counts():
    """Load up count tables"""

    map_category_list = ['Personal Theft/Larceny','Robbery', 'Rape/Sexual Assault','Aggravated Assault','Simple Assault','Other']
    hours_list = ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00",
                  "16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00"]
    day_list = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    month_list = ["January","February","March","April","May","June","July","August","September","October","November","December"]

    #iterate through items in hour, day, and month lists, and through categories to create the count tables according to the crime_stats database
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


if __name__ == "__main__":
    connect_to_db(app)

    #load_crime_stats()
    load_recent_stats()
    load_crime_counts()

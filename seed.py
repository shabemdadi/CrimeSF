"""Utility file to seed crime statistics and victim data"""

from model import Crime_Stat, Victim_Stat, Data_Import, connect_to_db, db
from server import app
import csv
from datetime import datetime
from sqlalchemy import desc
import requests


def load_crime_stats():
    """Load crime statistics from CSV file into database"""
    
    # variables in this dataset: 'IncidntNum','Category','Descript','DayOfWeek','Date','Time','PdDistrict','Resolution','Address','X','Y','Location'


    map_category_dict = {'LARCENY/THEFT':'Personal Theft/Larceny',
                         'BURGLARY':'Robbery',
                         'SEX OFFENSES, FORCIBLE':'Rape/Sexual Assault',
                         'VEHICLE THEFT':'Personal Theft/Larceny',
                         'ROBBERY':'Personal Theft/Larceny',
                         'ARSON':'Personal Theft/Larceny',
                         'STOLEN PROPERTY':'Personal Theft/Larceny',
                         'SEX OFFENSES, NON FORCIBLE':'Rape/Sexual Assault'
                         }

    with open('Data\Map__Crime_Incidents_-_from_1_Jan_2003.csv', 'rb') as f:
        reader = csv.reader(f)
    
        for i, row in enumerate(reader):
            if i > 0:
                incident_num = row[0]
                category = row[1]
                description = row[2]
                if category == "ASSAULT":
                    if "AGGRAVATED" in description:
                        map_category = "Aggravated assault"
                    else:
                        map_category = "Simple assault"
                else:
                    if category in map_category_dict:
                        map_category = map_category_dict[category]
                    else:
                        map_category = "Other"
                day_of_week = row[3]
                date_input = row[4]
                date = datetime.strptime(date_input, "%m/%d/%Y %H:%M:%S %p")
                time_input = row[5]
                time = datetime.strptime(time_input,"%H:%M").time()
                district = row[6]
                address = row[8]
                x_cord = row[9]
                y_cord = row[10]
                
                incident = Crime_Stat(incident_num=incident_num,category=category,description=description,map_category=map_category,day_of_week=day_of_week,date=date,time=time,
                    address=address,district=district,x_cord=x_cord,y_cord=y_cord)
                db.session.add(incident)
                if i % 1000 == 0:
                    db.session.commit()

        max_date = Crime_Stat.query.order_by(desc(Crime_Stat.date)).first().date
        data_import = Data_Import(max_date=max_date)
        db.session.add(data_import)

        db.session.commit()

def load_recent_stats():
    """Check API to see if there are new crime stats, if so, import into database."""

    map_category_dict = {'LARCENY/THEFT':'Personal Theft/Larceny',
                 'BURGLARY':'Robbery',
                 'SEX OFFENSES, FORCIBLE':'Rape/Sexual Assault',
                 'VEHICLE THEFT':'Personal Theft/Larceny',
                 'ROBBERY':'Personal Theft/Larceny',
                 'ARSON':'Personal Theft/Larceny',
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
                        map_category = "Aggravated assault"
                    else:
                        map_category = "Simple assault"
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

def load_victim_stats():
    """Load victim stats from csv file into database"""
    
    # variables in this dataset: 'ethnic1', 'weight', 'locationr', 'newoff', 'race1', 'notify', 'year', 'direl', 'marital2', 'treatment', 'hincome', 'injury', 
    #            'msa', 'vicservices', 'ethnic', 'newcrime', 'weapon', 'gender', 'age', 'popsize', 'hispanic', 'race', 'seriousviolent', 'region', 
    #            'weapcat'
    

    with open('Data\Victim_Stats.csv', 'rb') as f:
        reader = csv.reader(f)
                              
        for i, row in enumerate(reader):
            if i > 0:
                category = row[0]
                age_range = row[1]
                gender = row[2]
                percent = row[3]

                victim = Victim_Stat(age_range=age_range,gender=gender,category=category,percent=percent)
                db.session.add(victim)
        
        db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    #load_crime_stats()
    load_victim_stats()
    #load_recent_stats()

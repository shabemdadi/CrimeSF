"""Utility file to seed crime statistics and victim data"""

from model import Crime_Stat, Victim_Data, connect_to_db, db
from server import app
import csv
import datetime


def load_crime_stats():
    """Load crime statistics from CSV file into database"""
    
    # variables in this dataset: ['IncidntNum','Category','Descript','DayOfWeek','Date','Time','PdDistrict','Resolution','Address','X','Y','Location']
    
    with open('../Data/Map__Crime_Incidents_-_from_1_Jan_2003.csv', 'rb') as f:
        reader = csv.reader(f)
    
        for i,row in enumerate(reader):
            category = row[1]
            day_of_week = row[3]
            date_input = row[4]
            date = datetime.datetime.strptime(date_input, "%m/%d/%Y %I:%M")
            time = row[5]
            district = row[6]
            x_cord = row[9]
            y_cord = row[10]
            
            incident = Crime_Stat(category=category,day_of_week=day_of_week,date=date,time=time,district=district,x_cord=x_cord,y_cord=y_cord)
            db.session.add(incident)
            if i % 1000 == 0:
                db.session.commit()

        db.session.commit()

def load_victim_data():
    """Load victim data from JSON file into database"""
    
    # variables in this dataset: ['ethnic1', 'weight', 'locationr', 'newoff', 'race1', 'notify', 'year', 'direl', 'marital2', 'treatment', 'hincome', 'injury', 
    #            'msa', 'vicservices', 'ethnic', 'newcrime', 'weapon', 'gender', 'age', 'popsize', 'hispanic', 'race', 'seriousviolent', 'region', 
    #            'weapcat']
    
    with open('../Data/NCVS_2013_PERSONAL.csv', 'rb') as f:
        reader = csv.reader(f)
        
        rename_inputs_dict = {'age':{'1':(12,14),'2':(15,17),'3':(18,20),'4':(21,24),'5':(25,34),'6':(35,49),'7':(50,64),'8':(65,100)},
                              'gender':{'1':'Male','2':'Female'},
                              'newoff':{'1':'Rape/Sexual Assault', '2':'Robbery','3':'Aggravated Assault','4':'Simple Assault'}}
                              
        for row in reader:
            age_start = rename_inputs_dict['age'][row[6]][0]
            age_end = rename_inputs_dict['age'][row[6]][1]
            gender = rename_inputs_dict['gender'][row[2]]
            category = rename_inputs_dict['newoff'][row[19]]
            weight = row[1]
            
            victim = Victim_Data(age_start=age_start,age_end=age_end,gender=gender,category=category,weight=weight)
            db.session.add(victim)
        
        db.session.commit()
        

if __name__ == "__main__":
    connect_to_db(app)

    load_crime_stats()
    # load_victim_data()
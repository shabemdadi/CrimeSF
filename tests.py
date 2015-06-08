import unittest
from sqlalchemy import func
from model import Crime_Stat, Data_Import, Hour_Count, Day_Count, Month_Count, connect_to_db, db
from flask_sqlalchemy import SQLAlchemy

class TestMyAppUnitTestCase(unittest.TestCase):

    def setUp(self): #connect to the database
        from server import app
        connect_to_db(app)

    def test_stat_upload(self):		#make sure there are no duplicates of incident_num and category in our database
        self.assertFalse(Crime_Stat.query.with_entities(Crime_Stat.incident_num,Crime_Stat.category,func.count('*')).group_by(Crime_Stat.incident_num, Crime_Stat.category).having(func.count('*') > 1).all())

if __name__ == "__main__":
    unittest.main()


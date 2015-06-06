import unittest
from sqlalchemy import func
from model import Crime_Stat, Data_Import, Hour_Count, Day_Count, Month_Count, connect_to_db, db
from flask_sqlalchemy import SQLAlchemy

class TestMyAppUnitTestCase(unittest.TestCase):

    def setUp(self):
        print "set up is runnning"
        from server import app
        connect_to_db(app)

    def test_stat_upload(self):
        print "test is running"
        self.assertFalse(Crime_Stat.query.with_entities(Crime_Stat.incident_num,Crime_Stat.category,func.count('*')).group_by(Crime_Stat.incident_num, Crime_Stat.category).having(func.count('*') > 1).all())

if __name__ == "__main__":
    print "main is running"
    unittest.main()


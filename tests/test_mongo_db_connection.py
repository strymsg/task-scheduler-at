import sys
sys.path.append("C:\\Users\\ecris\\Desktop\AT_Bootcamp\\task-scheduler-at\\task_scheduler\\tasks")
from pymongo import MongoClient
from abstract_db_connector import MongoDbConnection
from unittest import TestCase

class TestMongoDbConnection(TestCase):

     def setUp(self):
        self.cases = [
                    MongoDbConnection(
                        db_name="dbtest1", 
                        db_host="localhost", 
                        username=None, 
                        password=None, 
                        port=27017),

                    MongoDbConnection(
                        db_name="dbtest1", 
                        db_host="localhost", 
                        username=None, 
                        password=None, 
                        port=27027)]

    def tearDown(self):
        del self.cases

    def test_connection(self):
        expected = ["Connection establish", "Connection Failure"]
        for i,j in enumerate(expected):
            self.assertEqual(self.cases[i],j)

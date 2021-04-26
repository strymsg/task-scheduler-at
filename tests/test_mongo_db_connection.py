from pymongo import MongoClient
from task_scheduler.tasks.abstract_db_connector import MongoDbConnection
from unittest import TestCase
import pytest


data = {
   "stock": "Brent Crude Futures",
   "qty": 510,
   "type": "buy-limit",
   "limit": 48.90,
   "client": "Crude Traders Inc."
   }

class TestMongoDbConnection(TestCase):

    """Test cases -> Multiple connection """
    # def setUp(self):
        
    #     self.cases = [
    #         MongoDbConnection(
    #             db_name="dbtest1", 
    #             db_host="localhost", 
    #             username=None, 
    #             password=None, 
    #             port=27017),

    #         MongoDbConnection(
    #             db_name="dbtest2", 
    #             db_host="localhost", 
    #             username=None, 
    #             password=None, 
    #             port=27017)
    #         ]
    
    # def tearDown(self):
    #     del self.cases


    """Test cases -> Single connection """
    def setUp(self):
        self.case_single_connection = MongoDbConnection(
                db_name="dbtest1", 
                db_host="localhost", 
                username=None, 
                password=None, 
                port=27017)
        
    def tearDown(self):
        del self.case_single_connection
        
    def test_multiple_connection(self):
        for instance, _ in enumerate(self.cases):
            self.assertEqual(self.cases[instance].connect(),"Connection Establish")

    def test_single_connection(self):
        self.assertEqual(self.case_single_connection.connect(),"Connection Establish")

    def test_insert_data_already_stored(self):
        self.case_single_connection.connect()
        expected = "This document already has this data"
        self.assertEqual(self.case_single_connection.insert(data), expected)

    def test_insert_new_data(self):
        self.case_single_connection.connect()
        self.assertEqual(self.case_single_connection.insert(data),True)

    def test_get_data(self):
        self.case_single_connection.connect()
        query = {"qty":510}
        self.assertEqual(self.case_single_connection.get(query),data)

    def test_delete_data(self):
        self.case_single_connection.connect()
        self.case_single_connection.insert(data)
        query = {"qty":510}
        self.assertEqual(self.case_single_connection.delete(query),1)

    def test_update_data(self):
        self.case_single_connection.connect()
        self.case_single_connection.insert(data)
        query = {"limit": {"$eq":48.90}}
        field = {"$inc":{"qty":+500}}
        self.assertEqual(self.case_single_connection.update(query,field),1)
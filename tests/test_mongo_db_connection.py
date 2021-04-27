from pymongo import MongoClient
from task_scheduler.tasks.abstract_db_connector import MongoDbConnection
from unittest import TestCase
import pytest
import unittest

data = {
   "stock": "Brent Crude Futures",
   "qty": 510,
   "type": "buy-limit",
   "limit": 48.90,
   "client": "Crude Traders Inc."
   }

# Test cases -> Multiple connectio
new_data = {
   "stock": "Brent Crude Futures",
   "qty": 910,
   "type": "buy-limit",
   "limit": 48.90,
   "client": "Crude Traders Inc."
   }

# Test cases -> Single connection
cases = [
            MongoDbConnection(
                db_name="dbtest1", 
                db_host="localhost", 
                username=None, 
                password=None, 
                port=27017),

            MongoDbConnection(
                db_name="dbtest2", 
                db_host="localhost", 
                username=None, 
                password=None, 
                port=27017)
            ]

case_single_connection = cases [0]

class TestMongoDbConnection(TestCase):
      
    def test_multiple_connection(self):
        for instance, _ in enumerate(cases):
            self.assertEqual(cases[instance].connect(),"Connection Establish")

    def test_single_connection(self):
        self.assertEqual(case_single_connection.connect(),"Connection Establish")

    def test_insert_data_already_stored(self):
        case_single_connection.connect()
        case_single_connection.insert(data)
        expected = "This document already has this data"
        self.assertEqual(case_single_connection.insert(data), expected)
        case_single_connection.delete({"qty":510})

    def test_insert_new_data(self):
        case_single_connection.connect()
        self.assertEqual(case_single_connection.insert(new_data),True)
        case_single_connection.delete({"qty":910})

    def test_get_data(self):
        expected = {
            "stock": "Brent Crude Futures",
            "qty": 510,
            "type": "buy-limit",
            "limit": 48.90,
            "client": "Crude Traders Inc."
            }
        case_single_connection.connect()
        case_single_connection.insert(data)
        query = {"limit": {"$eq":48.90}}
        self.assertEqual(case_single_connection.get(query),expected)

    def test_delete_data(self):
        case_single_connection.connect()
        case_single_connection.insert(data)
        query = {"qty":510}
        self.assertEqual(case_single_connection.delete(query),1)

    def test_update_data(self):
        case_single_connection.connect()
        case_single_connection.insert(data)
        query = {"limit": {"$eq":48.90}}
        field = {"$set":{"limit":50}}
        self.assertEqual(case_single_connection.update(query,field),1)
        case_single_connection.delete({"limit":50})

if __name__ == "__main__":
    unittest.main()
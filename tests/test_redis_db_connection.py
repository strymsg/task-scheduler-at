from redis import Redis
from task_scheduler.tasks.abstract_db_connector import RedisDbConnection
from unittest import TestCase
import pytest



data = {
   "stock": "Brent Crude Futures",
   "qty": 510,
   "type": "buy-limit",
   "limit": 48.90,
   "client": "Crude Traders Inc."
   }

class TestRedisDbConnection(TestCase):

    """Test cases -> Multiple connection """
    # def setUp(self):
        
    #     self.cases = [
    #         RedisDbConnection(
    #             db_name="0", 
    #             db_host="localhost", 
    #             username=None, 
    #             password=None, 
    #             port=6379),

    #         RedisDbConnection(
    #             db_name="1", 
    #             db_host="localhost", 
    #             username=None, 
    #             password=None, 
    #             port=6379),
    #         ]

    # def tearDown(self):
    #     del self.cases


    """Test cases -> Single connection """
    def setUp(self):
        self.case_single_connection = RedisDbConnection(
                db_name="0", 
                db_host="localhost", 
                username=None, 
                password=None, 
                port=6379)
    
    def tearDown(self):
        del self.case_single_connection
        
    def test_multiple_connection(self):
        for instance in self.cases:
            self.assertIsInstance(instance, RedisDbConnection)

    def test_single_connection(self):
        self.assertEqual(self.case_single_connection.connect(),"Connection Establish")

    def test_insert_data_already_stored(self):
        self.case_single_connection.connect()
        expected = "This document already has this data"
        self.assertEqual(self.case_single_connection.insert(data, "DATA1"), expected)

    def test_insert_new_data(self):
        self.case_single_connection.connect()
        self.assertTrue(self.case_single_connection.insert(data, "DATA1"))

    def test_get_data(self):
        self.case_single_connection.connect()
        query = "DATA1"
        self.assertEqual(self.case_single_connection.get(query),data)

    def test_delete_data(self):
        self.case_single_connection.connect()
        self.case_single_connection.insert(data, "DATA1")
        query = "DATA1"
        expected = "Delete operation was successful"
        self.assertEqual(self.case_single_connection.delete(query), expected)

    # def test_update_data(self):
    #     self.case_single_connection.connect()
    #     self.case_single_connection.insert(data)
    #     query = {"limit": {"$eq":48.90}}
    #     field = {"$inc":{"qty":+500}}
    #     self.assertEqual(self.case_single_connection.update(query,field),1)
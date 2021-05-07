from redis import Redis
from task_scheduler.tasks.abstract_db_connector import RedisDbConnection
from task_scheduler.utils.exceptions import DbErrorHandler
from unittest import TestCase
import pytest
import unittest

data = {
    "stock": "Brent Crude Futures",
    "qty": 510,
    "type": "buy-limit",
    "limit": 48.9,
    "client": "Crude Traders Inc."
}

# Test cases -> Multiple connection
new_data = {
    "stock": "Brent Crude Futures",
    "qty": 910,
    "type": "buy-limit",
    "limit": 48.90,
    "client": "Crude Traders Inc."
}

# Test cases -> Single connection
cases = [
    RedisDbConnection(
        db_name="0",
        db_host="localhost",
        username=None,
        password=None,
        port=6379),

    RedisDbConnection(
        db_name="1",
        db_host="localhost",
        username=None,
        password=None,
        port=6379)
]

case_single_connection = cases[0]


class TestRedisDbConnection(TestCase):

    def test_multiple_connection(self):
        for instance, _ in enumerate(cases):
            self.assertEqual(cases[instance].connect(), "Connection Established")

    def test_single_connection(self):
        self.assertEqual(case_single_connection.connect(), "Connection Established")

    def test_insert_data_already_stored(self):
        with self.assertRaises(DbErrorHandler) as cm:
            case_single_connection.connect()
            case_single_connection.insert(data, "config-1")
            expected = "This document already has this data"
            self.assertEqual(case_single_connection.insert(data, "config-1"), expected)
        case_single_connection.delete("config-1")

    def test_insert_new_data(self):
        case_single_connection.connect()
        expected = "Data successfully created"
        self.assertEqual(case_single_connection.insert(new_data, "config-2"), expected)
        case_single_connection.delete("config-2")

    def test_get_data(self):
        expected = {
            "stock": "Brent Crude Futures",
            "qty": "510",
            "type": "buy-limit",
            "limit": "48.9",
            "client": "Crude Traders Inc."
        }
        case_single_connection.connect()
        case_single_connection.insert(data, "config-1")
        query = "config-1"
        self.assertEqual(case_single_connection.get(query)[query], expected)

    def test_delete_data(self):
        with self.assertRaises(DbErrorHandler) as cm:
            case_single_connection.connect()
            expected = "Nothing found to delete"
            self.assertEqual(case_single_connection.delete("conf-1pol"), expected)

    # def test_update_data(self):
    #     case_single_connection.connect()
    #     case_single_connection.insert(data)
    #     query = {"limit": {"$eq":48.90}}
    #     field = {"$inc":{"qty":+500}}
    #     self.assertEqual(case_single_connection.update(query,field),1)


if __name__ == "__main__":
    unittest.main()

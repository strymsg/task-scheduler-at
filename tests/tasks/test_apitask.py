from unittest import TestCase
import pytest

from task_scheduler.tasks.api_request_task import ApiRequestTask
from task_scheduler.tasks.config_objects import ConfigApiRequestTask

class TestApiTask(TestCase):
    def setUp(self):
        self.config_api_get = ConfigApiRequestTask(
            'https://api.github.com', http_method='get')
        self.config_api_post = ConfigApiRequestTask(
            'https://reqbin.com/echo/post/json',
            http_method='post',
            headers={ 'Accept': 'application/json', 'Content-Type': 'application/json'},
            body={
                "Id": 78912,
                "Customer": "Jason Sweet",
                "Quantity": 1,
                "Price": 18.00
        })
        self.config_api_patch = ConfigApiRequestTask(
            'https://httpbin.org/patch',
            http_method='patch',
            headers={ 'Accept': 'application/json', 'Content-Type': 'application/json'},
            body={ 'key': 'value' })
        self.config_api_delete = ConfigApiRequestTask(
            'https://httpbin.org/delete',
             http_method='delete')

    def tearDown(self):
        self.config_api_get = None
        self.config_api_delete = None
        self.config_api_patch = None
        self.config_api_post = None
    #
    # def test_log(self):
    #     api_task = ApiRequestTask(0, config=self.config_api_get)
    #     # checking log entry
    #     with open('file.log') as f:
    #         cont = f.read()
    #         print(f,'\n--*****************---')
    #         print(api_task.task_id)
    #         self.assertTrue(cont.endswith(api_task.task_id))

    def test_get_request1(self):
        api_task = ApiRequestTask(0, config=self.config_api_get)
        resp = api_task.execute()
        self.assertEqual(resp['url'], 'https://api.github.com/')
        expected_keys = ['json', 'text', 'status_code', 'headers', 'url']
        for expected_key in expected_keys:
            self.assertTrue(expected_key in resp.keys())

    def test_post_request(self):
        api_task = ApiRequestTask(0, config=self.config_api_post)
        resp = api_task.execute()
        # print(resp)
        self.assertEqual(resp['status_code'], 200)

    def test_patch_request(self):
        api_task = ApiRequestTask(0, config=self.config_api_patch)
        resp = api_task.execute()
        self.assertEqual(resp['status_code'], 200)

    def test_delete_request(self):
        api_task = ApiRequestTask(0, config=self.config_api_delete)
        resp = api_task.execute()
        self.assertEqual(resp['status_code'], 200)

    def test_get_notfound(self):
        config = ConfigApiRequestTask(
            'https://api.github.com/inex',
            http_method='get')
        api_task = ApiRequestTask(0, config=config)
        resp = api_task.execute()
        self.assertEqual(resp['status_code'], 404)

    def test_request_fail1(self):
        config = ConfigApiRequestTask(
            'https://api.nutexis.cualquiercosa',
            http_method='get')
        api_task = ApiRequestTask(0, config=config)
        try:
            resp = api_task.execute()
            self.assertTrue(resp is None)
        except ConnectionError as conn_err:
            assert True
        except Exception as err:
            self.assertNotEqual(
                type(err),
                "<class 'requests.exceptions.ConnectionError'>")




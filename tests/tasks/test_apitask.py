import pytest

from task_scheduler.tasks.api_request_task import ApiRequestTask
from task_scheduler.tasks.config_objects import ConfigApiRequestTask

@pytest.fixture
def config_api_get():
    config = ConfigApiRequestTask('https://api.github.com', http_method='get')
    return config

@pytest.fixture
def config_api_post():
    config = ConfigApiRequestTask(
        'https://reqbin.com/echo/post/json',
        http_method='post',
        headers={ 'Accept': 'application/json', 'Content-Type': 'application/json'},
        body={
            "Id": 78912,
            "Customer": "Jason Sweet",
            "Quantity": 1,
            "Price": 18.00
        })
    return config

@pytest.fixture
def api_task(config_api_get):
    apitask = ApiRequestTask(0, config=config_api_get)
    return apitask

def test_apitask(api_task):
    assert api_task.config.url == 'https://api.github.com'

def test_get_request1(api_task):
    resp = api_task.execute()
    #print(resp, type(resp))
    assert resp['url'] == 'https://api.github.com/'
    expected_keys = ['json', 'text','status_code','headers','url']
    for expected_key in expected_keys:
        assert expected_key in resp.keys()

def test_post_request(config_api_post):
    api_task = ApiRequestTask(0, config=config_api_post)
    resp = api_task.execute()
    # print(resp)
    assert resp['status_code'] == 200

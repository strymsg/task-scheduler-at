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
def config_api_patch():
    config = ConfigApiRequestTask(
        'https://httpbin.org/patch',
        http_method='patch',
        headers={ 'Accept': 'application/json', 'Content-Type': 'application/json'},
        body={ 'key': 'value' })
    return config

@pytest.fixture
def config_api_delete():
    config = ConfigApiRequestTask(
        'https://httpbin.org/delete',
        http_method='delete')
    return config

@pytest.fixture
def api_task(config_api_get):
    apitask = ApiRequestTask(0, config=config_api_get)
    assert apitask.task_id != ''
    #print('id:', apitask.task_id)
    return apitask

def test_apitask(api_task):
    assert api_task.config.url == 'https://api.github.com'

def test_get_request1(api_task):
    resp = api_task.execute()
    assert resp['url'] == 'https://api.github.com/'
    expected_keys = ['json', 'text','status_code','headers','url']
    for expected_key in expected_keys:
        assert expected_key in resp.keys()

def test_post_request(config_api_post):
    api_task = ApiRequestTask(0, config=config_api_post)
    resp = api_task.execute()
    # print(resp)
    assert resp['status_code'] == 200

def test_patch_request(config_api_patch):
    api_task = ApiRequestTask(0, config=config_api_patch)
    resp = api_task.execute()
    assert resp['status_code'] == 200

def test_delete_request(config_api_delete):
    api_task = ApiRequestTask(0, config=config_api_delete)
    resp = api_task.execute()
    assert resp['status_code'] == 200

def test_get_notfound():
    config = ConfigApiRequestTask('https://api.github.com/inex', http_method='get')
    api_task = ApiRequestTask(0, config=config)
    resp = api_task.execute()
    assert resp['status_code'] == 404

def test_request_fail1():
    config = ConfigApiRequestTask('https://api.nutexis.cualquiercosa', http_method='get')
    api_task = ApiRequestTask(0, config=config)
    try:
        resp = api_task.execute()
        assert resp is None
    except ConnectionError as conn_err:
        assert True
    except Exception as err:
        assert type(err) != "<class 'requests.exceptions.ConnectionError'>"
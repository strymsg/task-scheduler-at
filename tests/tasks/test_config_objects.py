import pytest

from task_scheduler.tasks.config_objects import  ConfigObject, ConfigDbTask, ConfigFileTask, ConfigApiRequestTask


@pytest.fixture
def config_api():
    config = ConfigApiRequestTask('https://api.github.com', http_method='get')
    return config

def test_init_api(config_api):
    assert config_api.url == 'https://api.github.com'
    assert config_api.http_method == 'get'

    assert config_api.config_id == ''
    config_api.config_id = '01'
    assert config_api.config_id == '01'

def test_config_api(config_api):
    config_api.config({ 'url': 'https://wikipedia.org', 'http_method': 'GET'})
    assert config_api.url == 'https://wikipedia.org'
    assert config_api.http_method == 'GET'
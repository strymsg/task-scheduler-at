import pytest

from task_scheduler.tasks.config_objects import  ConfigObject, ConfigDbTask, ConfigFileTask, ConfigApiRequestTask

def test_instantiate_configapirequest():
    config = ConfigApiRequestTask('https://api.github.com', http_method='get')
    print(config)
    assert config.url == 'https://api.github.com'
    assert config.http_method == 'get'
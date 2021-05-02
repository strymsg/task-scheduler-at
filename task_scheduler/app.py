__version__ = "0.0.2"
import os
import logging
from flask import Flask

from task_scheduler.configs.config import Configuration
from task_scheduler.utils.logger import CustomLogger
from task_scheduler.endpoints.api_request_tasks import bp_tasks

def config_logger(config):
    '''Configures Logger using the config dict and CustomLogger

    :param config: dictionary with configuration parameters
    :return:
    '''
    logger = CustomLogger(__name__, config)
    return logger

def create_app(test_config=None):
    import pprint
    app = Flask(__name__)
    print("create_app()")
    config_obj = Configuration()

    logger = config_logger(config_obj.configuration)
    app.config.from_mapping(
        SECRET_KEY=config_obj.get_config_var('secret_key'),
    )
    logger.info("INITIALIZED TASK SCHEDULER APP")

    # registering blueprints for endpoints on different modules
    app.register_blueprint(bp_tasks)

    print("------ endpoints ------")
    for rule in app.url_map.iter_rules():
        print(f'{rule.rule}: {rule.endpoint}')
    print()

    return app


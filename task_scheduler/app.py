__version__ = "0.0.2"
import os
import logging
from flask import Flask

from task_scheduler.configs.config import Configuration
from task_scheduler.utils.logger import CustomLogger
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_restful import Resource, Api, reqparse
#from task_scheduler.endpoints.api_request_tasks import bp_tasks
from task_scheduler.endpoints.api_request_tasks import ApiRequestTaskByIdEndpoint, \
    ApiRequestTasksEndpoint, ApiRequestTaskExecEndpoint
from task_scheduler.utils.constants import API_ROUTES


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

    app.config.update(
        {
            'APISPEC_SPEC': APISpec(
            title='Task Scheduler',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'),
            'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
            'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
        })

    # restful api to manage endpoints
    api = Api(app)
    docs = FlaskApiSpec(app)
    api.add_resource(ApiRequestTaskExecEndpoint, API_ROUTES['TASK_API_EXECUTE'])
    api.add_resource(ApiRequestTasksEndpoint, API_ROUTES['TASKS'])
    api.add_resource(ApiRequestTaskByIdEndpoint, API_ROUTES['TASK'] + '<string:task_id>')

    logger = config_logger(config_obj.configuration)
    app.config.from_mapping(
        SECRET_KEY=config_obj.get_config_var('secret_key'),
    )
    logger.info("INITIALIZED TASK SCHEDULER APP")

    # registering blueprints for endpoints on different modules
    # app.register_blueprint(bp_tasks)
    #
    print("------ endpoints ------")
    for rule in app.url_map.iter_rules():
        print(f'{rule.rule}: {rule.endpoint}')



    return app


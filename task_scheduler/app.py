__version__ = "0.0.3"
import os
import logging
from flask import Flask, g
from task_scheduler.configs.config import Configuration
from task_scheduler.utils.logger import CustomLogger
from apispec import APISpec

from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_restful import Resource, Api, reqparse

from task_scheduler.endpoints.api_request_tasks import ApiRequestTaskByIdEndpoint, \
    ApiRequestTasksEndpoint, ApiRequestTaskExecEndpoint
from task_scheduler.endpoints.db_task_endpoint \
                            import DbTaskEndpoint
from task_scheduler.utils.constants import API_ROUTES, HOST_MONGO

from task_scheduler.tasks.abstract_db_connector import MongoDbConnection

def config_logger(config):
    '''Configures Logger using the config dict and CustomLogger

    :param config: dictionary with configuration parameters
    :return:
    '''
    logger = CustomLogger(__name__, config)
    return logger

def init_db(app, db_configs):
    # connection to the mongo database
    if 'db' not in g:
        mongo_connection = MongoDbConnection(
            db_name=db_configs['name'],
            username=db_configs['username'],
            db_host=db_configs['host'],
            password=db_configs['password'],
            port=db_configs['port']
            )
        g.db = mongo_connection
        app.mongo_connection = mongo_connection
        print("Configs::::::")
        print(db_configs)
    return g.db


def create_app(test_config=None):
    import pprint
    app = Flask(__name__)
    print("create_app()")
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
    api.add_resource(ApiRequestTaskExecEndpoint, API_ROUTES['API_TASK_EXECUTE'])
    api.add_resource(ApiRequestTasksEndpoint, API_ROUTES['API_TASK_ALL'])
    api.add_resource(ApiRequestTaskByIdEndpoint, API_ROUTES['API_TASK'] + '/<string:task_id>')
    api.add_resource(DbTaskEndpoint, API_ROUTES["DB_TASK"])
    docs.register(ApiRequestTasksEndpoint)
    docs.register(ApiRequestTaskExecEndpoint)
    docs.register(ApiRequestTaskByIdEndpoint)
    docs.register(DbTaskEndpoint)

    config_obj = Configuration()

    _logger = config_logger(config_obj.configuration)
    app.config.from_mapping(
        SECRET_KEY=config_obj.get_config_var('secret_key'),
    )
    _logger.info("INITIALIZED TASK SCHEDULER APP")

    print("------ endpoints ------")
    for rule in app.url_map.iter_rules():
        print(f'{rule.rule}: {rule.endpoint}')
    print()
    with app.app_context():
        init_db(app, config_obj.get_config_var('app_db'))

    return app

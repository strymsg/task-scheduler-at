__version__ = "0.0.1"
import os
import logging
from flask import Flask, request, g
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_restful import Resource, Api, reqparse
from flask_apispec.extension import FlaskApiSpec
from task_scheduler.configs.config import Configuration
from task_scheduler.utils.logger import CustomLogger
from task_scheduler.endpoints.db_task_endpoint \
                            import DbTaskEndpoint, DbTaskEndpointById
from task_scheduler.utils.constants import API_ROUTES
from task_scheduler.tasks.abstract_db_connector import MongoDbConnection

def config_logger(config):
    """Configures Logger using the config dict and CustomLogger
    :param config: dictionary with configuration parameters
    :return:
    """
    logger = CustomLogger(__name__, config)
    return logger

def init_db(app, db_configs):
    # connection to the mongo database
    if 'db' not in g:
        mongo_connection = MongoDbConnection(
            db_name=db_configs['name'],
            username=db_configs['username'],
            db_host='localhost',
            password=db_configs['password'],
            port=db_configs['port']
            )
        g.db = mongo_connection
        app.mongo_connection = mongo_connection
    return g.db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Task Scheduler',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
    })
    config_obj = Configuration()

    logger = config_logger(config_obj.configuration)
    app.config.from_mapping(
        SECRET_KEY=config_obj.get_config_var('secret_key'),
    )
    logger.info("INITIALIZED TASK SCHEDULER APP")

    api = Api(app)  # Flask restful wraps Flask app around it.
    docs = FlaskApiSpec(app)    
    api.add_resource(DbTaskEndpoint, API_ROUTES["DB_TASK"])
    api.add_resource(DbTaskEndpointById, API_ROUTES["DB_TASK_BY_ID"])
    docs.register(DbTaskEndpoint)
    docs.register(DbTaskEndpointById)

    with app.app_context():
        init_db(app, config_obj.get_config_var('app_db'))

    return app

app = create_app()
__version__ = "0.0.1"
import os
import logging
from flask import Flask, request
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_restful import Resource, Api, reqparse
from flask_apispec.extension import FlaskApiSpec
from task_scheduler.configs.config import Configuration
from task_scheduler.utils.logger import CustomLogger
from task_scheduler.endpoints.db_task_endpoint \
                            import DbTaskEndpoint, DbTaskEndpointById
from task_scheduler.utils.constants import API_ROUTES

def config_logger(config):
    """Configures Logger using the config dict and CustomLogger
    :param config: dictionary with configuration parameters
    :return:
    """
    logger = CustomLogger(__name__, config)
    return logger

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
    api.add_resource(DbTaskEndpointById, API_ROUTES["DB_TASK"]+'/<string:by_id>')
    docs.register(DbTaskEndpoint)
    docs.register(DbTaskEndpointById)

    return app

app = create_app()
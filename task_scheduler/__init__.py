"""
Task Manager and Scheduler
"""

__version__ = "0.0.1"
import os
import logging
from flask import Flask

from task_scheduler.configs.config import Configuration
from task_scheduler.utils.logger import CustomLogger

def config_logger(config):
      logger = CustomLogger(__name__, config)
      return logger

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    print("task scheduler...")
    config_obj = Configuration()

    logger = config_logger(config_obj.configuration)
    #logger.info(f'Configurations loaded {config_obj.configuration}')
    #logger.info("logging info test")
    #logger.error("logging Error test")
    #logger.debug("logging debug test")
    app.config.from_mapping(
        SECRET_KEY=config_obj.get_config_var('secret_key'),
    )
    logger.info("INITIALIZED TASK SCHEDULER APP")

    # testing purposes
    #from task_scheduler.tasks.abstract_task import AbstractTask
    #at = AbstractTask(0, 'Request...')

    return app
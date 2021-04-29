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
    app.config.from_mapping(
        SECRET_KEY=config_obj.get_config_var('secret_key'),
    )
    logger.info("INITIALIZED TASK SCHEDULER APP")

    return app
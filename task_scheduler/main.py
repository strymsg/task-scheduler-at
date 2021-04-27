import sys

from flask import Flask
from utils.logger import CustomLogger
app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'Index Page Custom'
#
# @app.route('/hello')
# def hello():
#     return 'Hello, World'
#
#
# @app.errorhandler(404)
# def page_not_found(e):
#     return "<h1>404</h1><p>The resource could not be found. Custom page</p>", 40

def basic_login():
    import logging
    # logging.basicConfig()
    logging.basicConfig(format='custom: %(process)d-%(levelname)s-%(message)s',
                        level=logging.DEBUG)
    logging.info('task scheduler Started')
    try:
        c = 2 / 0
    except Exception as e:
        logging.error("Error logger ...")
        logging.exception("Exception logger ...")


if __name__ == "__main__":
    # basic_login()

    logger = CustomLogger(__name__)
    # logger.info("testing")
    # logger.error("errrrrr")
    # logger.debug("asadsa")

    ### pruebas
    #import utils
    #utils.logger.info("testing")
    #utils.logger.error("errrrrr")
    #utils.logger.debug("dddddddddddddddddd")

    #from tasks.config_objects import ConfigApiRequestTask
    from task_scheduler.tasks.config_objects import ConfigApiRequestTask, ConfigApiRequestTask
    config = ConfigApiRequestTask('https://api.github.com', http_method='get')

    app.run(host='0.0.0.0', debug=True, port=5000)



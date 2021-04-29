# there should be a configuration class that can return data about:
#- the db port of my db for my application
#- the ip/hostname of my db db for my application
#- the log level for my custom logger (this is for the Customlogger to consume)
import os
import json
from json import JSONDecodeError

class Configuration:
    '''Loads the configuration json file (depending on FLASK_ENV variable)
     and returns a dict. If loading fails prints error and returns enmpty dict
    '''
    def __init__(self):
        self.configuration = {}
        filename = os.path.join(os.path.abspath(os.path.dirname(__file__)))
        if os.environ.get('FLASK_ENV') == 'development':
            filename = os.path.join(filename, 'config.dev.json')
        else:
            filename = os.path.join(filename, 'config.prod.json')

        with open(filename) as jsonfile:
            try:
                d = json.loads(jsonfile.read())
                self.configuration = d
            except JSONDecodeError as err:
                print(f"Error decoding json {jsonfile.name}")
                print(err)

    def get_config_var(self, var_name, default_value=None):
        return self.configuration.get(var_name, default_value)


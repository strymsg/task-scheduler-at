import requests
from requests.exceptions import HTTPError, ConnectionError, RequestException
from requests.exceptions import URLRequired

from json import JSONDecodeError

from task_scheduler.tasks.abstract_task import AbstractTask
from task_scheduler.tasks.config_objects import ConfigApiRequestTask

class ApiRequestTask(AbstractTask):
    def __init__(self, priority, config:ConfigApiRequestTask):
        ''' Instantiates an Api request task
        :param priority: from 0 (most important) to any greater integer
        :param config(ConfigApiRequestTask): Configuration parameters
        '''
        super().__init__(priority, type='Api-request')
        self.config = config

    def do_request(self):
        '''Do api request using requests library using config object
        :return: dict with response objects cotaining:
        { 
          'json': <dict>, # json convertion or {}
          'text': <str>,  # string response
          'status_code': <str>, 
          'headers': <dict>,
          'url': <str>
         }
        If an error occurs it raises an HTTPError exceptio
        '''
        if self.config is None:
            raise Exception("Need a config object to do request")

        response = None
        try:
            # TODO: add support to send api_token
            response = requests.request(
                self.config.http_method.upper(),
                self.config.url,
                params=None,
                data=self.config.body,
                headers=self.config.headers,
                cookies=None,
                files=None,
                auth=None,
                timeout=None,
                allow_redirects=True,
                proxies=None,
                hooks=None,
                stream=None,
                verify=None,
                cert=None
            )
            response_json = {}
            try:
                response_json = response.json()
            except JSONDecodeError as json_err:
                pass
            res_dict = {
                'json': response_json,
                'text': response.text,
                'status_code': response.status_code,
                'headers': response.headers,
                'url': response.url
            }
            return res_dict
        # TODO: Log all exceptions
        except HTTPError as http_err:
            print(f'HTTPError: {http_err}')
            raise http_err
        except RequestException as request_err:
            print(f'HTTPError: {request_err}')
            raise request_err
        except ConnectionError as conn_err:
            print(f'HTTPError: {conn_err}')
            raise conn_err
        except URLRequired as url_err: 
            print(f'HTTPError: {url_err}')
            raise url_err

    def execute(self):
        ''' Performs an API request and returns 
        a dictionary with response results or raises exception
        '''
        try:
            response = self.do_request()
            return response
        except Exception as E:
            raise E

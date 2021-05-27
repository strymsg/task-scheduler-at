import json
import os
from datetime import datetime
from flask import request, jsonify, make_response, current_app
from flask_restful import Resource, request
from flask_apispec import doc
from flask_apispec.views import MethodResource

class HelloMessage(MethodResource):
    @doc(description='', tags=['Hello Message'])
    def get(self):
        message = {
            'message': 'Hello AT bootcamp',
            'environment': os.environ.get('FLASK_ENV', 'Not specified'),
            'time': str(datetime.now())
        }
        return message
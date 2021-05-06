# Source: https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

#JSONEncoder().encode(analytics)
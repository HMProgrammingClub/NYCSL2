import json
import datetime
from bson.objectid import ObjectId
from werkzeug import Response

class MongoJsonEncoder(json.JSONEncoder):
    """Json encoder with support for MongoDB ObjectId"""
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def jsonify(*args):
    """jsonify with support for MongoDB ObjectId"""
    return Response(json.dumps(*args, cls=MongoJsonEncoder), mimetype='application/json')

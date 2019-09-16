from flask_restful import Resource
from flask_restful import Api

class ScanAPI(Resource):

    def get(self, location):
        return {'test':True}

    def post(self, location):
        return {'test':True}


# Get list of missing people
# WebSocket for tracking scans live


def register(app):
    api = Api(app, prefix='/api/v1')
    api.add_resource(ScanAPI, '/scan/<string:location>', endpoint='scan')

import uuid
import arrow

from flask_restful import Resource
from flask_restful import Api
from flask_restful import reqparse, fields, marshal_with

from flask import url_for

class ScanAPI(Resource):

    def get(self, location):
        return {'test':True}

    def post(self, location):
        return {'test':True}

location_output = {
    'url': fields.Url(endpoint='location'),
    'id': fields.String,
    'name': fields.String,
}

location_list_output = {
    'locations': fields.List(fields.Nested(location_output))
}

location_create_parser = reqparse.RequestParser(bundle_errors=True)
location_create_parser.add_argument('name', required=True, help="Name cannot be blank")
class LocationListAPI(Resource):
    @marshal_with(location_list_output)
    def get(self):
        import model

        res = []

        for loc in model.Location.query.all():
            res.append({
                'url': loc,
                'id': loc.id,
                'name': loc.name,
            })

        return {'locations': res}

    def post(self):
        import model
        from main import db

        args = location_create_parser.parse_args()

        loc = model.Location()

        loc.id = uuid.uuid4()
        loc.name = args.get('name')

        db.session.add(loc)
        db.session.commit()

        return args

class LocationAPI(Resource):
    @marshal_with(location_output)
    def get(self, id):
        import model

        loc = model.Location.query.filter_by(id=id).first()

        return {
            'url': loc,
            'id': loc.id,
            'name': loc.name,
        }

    def put(self, id):
        pass


event_output = {
    'url': fields.Url('event'),
    'id': fields.String,
    'name': fields.String,
    'start': fields.String,
    'end': fields.String,
    'location': fields.Url('location'),
    'groups': fields.List(fields.Url('group')),
}
event_list_output = fields.List(fields.Nested(event_output))

event_create_parser = reqparse.RequestParser(bundle_errors=True)
event_create_parser.add_argument('name', required=True, help="Name cannot be blank")
event_create_parser.add_argument('start', required=True)
event_create_parser.add_argument('end', required=True)

class LocationEventsAPI(Resource):
    @marshal_with(event_list_output)
    def get(self, location):
        import model
        loc = model.Location.query.filter_by(id=location).first()

        return loc.events

    @marshal_with(event_output)
    def post(self, location):
        args = event_create_parser.parse_args()

        import model
        loc = model.Location.query.filter_by(id=location).first()

        evt = model.Event()
        evt.name = args.get('name')
        evt.start = args.get('start')
        evt.end = args.get('end')
        evt.id = uuid.uuid4()
        evt.location = loc

        from main import db
        db.session.add(evt)
        db.session.commit()

        return {
            'url': evt,
            'id': evt.id,
            'name': evt.name,
            'start': evt.start,
            'end': evt.end,
            'location': loc,
            'groups': [],
        }



class EventAPI(Resource):
    @marshal_with(event_output)
    def get(self, id):
        import model
        evt = model.Event.query.filter_by(id=id).first()

        return {
            'url': evt,
            'id': evt.id,
            'name': evt.name,
            'start': evt.start,
            'end': evt.end,
            'location': evt.location,
            'groups': evt.groups,
        }

    @marshal_with(event_output)
    def put(self, id):
        pass

# Get list of missing people
# WebSocket for tracking scans live
# Add/Edit/Delete location
# Add/Edit/Delete person
# Add/Edit/Delete group
# Add/Edit/Delete event
# List events (all, per-group, per-user, filter by time)
# List locations


def register(app):
    api = Api(app, prefix='/api/v1')
    api.add_resource(ScanAPI, '/scan/<uuid:location>', endpoint='scan')
    api.add_resource(LocationListAPI, '/location', endpoint='locations')
    api.add_resource(LocationAPI, '/location/<uuid:id>', endpoint='location')
    api.add_resource(LocationEventsAPI, '/location/<uuid:location>/events', endpoint='location_events')
    api.add_resource(EventAPI, '/event/<uuid:id>/events', endpoint='event')

#import model

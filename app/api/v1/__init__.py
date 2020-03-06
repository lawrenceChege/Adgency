from flask import Blueprint
from werkzeug.exceptions import MethodNotAllowed, Forbidden, BadRequest
from flask_restplus import Api
from flask_jwt_extended.exceptions import NoAuthorizationError
from app.api.v1.views.users import Users, User, ViewUsers, ManageUsers
from app.api.v1.views.concept import Concepts
# from twilio.base.exceptions import TwilioRestException

version_one = Blueprint("v1", __name__, url_prefix="/api")
API = Api(version_one, catch_all_404s= True)


# API.add_resource(Status, '/incidents/<int:incident_id>/status')
API.add_resource(Users, '/signup/')
API.add_resource(User, '/login/')
API.add_resource(ViewUsers, '/users/')
API.add_resource(Concepts, '/client/concept/')



@API.errorhandler
def default_error_handler(error):
    '''Default error handler'''
    return {'status': 500,'message': str(error)}, getattr(error, 'code', 500)


@API.errorhandler(NoAuthorizationError)
def handle_Missing_Token_exception(error):
    '''Return a custom message and 401 status code'''
    return {'status': 401,'message': str(error)}, 401

@API.errorhandler(MethodNotAllowed)
def handle_Method_Not_Allowed(error):
    '''Return a custom message and 405 status code'''
    return {'status': 405,'error': 'Method is not allowed on this url'}, 405

@API.errorhandler(Forbidden)
def handle_Forbidden(error):
    '''Return a custom message and 403 status code'''
    return {'status': 403,'error': 'This door is staff only'}, 403


@API.errorhandler(BadRequest)
def handle_Bad_Request(error):
    '''Return a custom message and 400 status code'''
    return {'status': 400,'error': 'This is a bad request. Check your data'}, 400

# @API.errorhandler(TwilioRestException)
# def handle_Bad_phone(error):
#     '''Return a custom message and 400 status code'''
#     return {'status': 21608,'message': 'The thing is... This is a free account. No sms to you'}, 21608
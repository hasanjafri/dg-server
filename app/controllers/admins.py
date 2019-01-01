""" Admins controller using Sanic Class based views. """

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin
from app.utils.auth import get_salt

class AdminController(HTTPMethodView):
    """ Handles Admin CRUD operations. """
    
    async def get(self, request):
        pass
    
    async def post(self, request):
        for param in ['email', 'password', 'firstName', 'lastName', 'phoneNum', 'country', 'countryCode', 'bday', 'tier', 'period']:
            if request.json[param] == "":
                return json({'error': '{} field cannot be blank!'.format(param)})
        
        with scoped_session() as session:
            admin = Admin(
                email=request.json.get('email'),
                password=request.json.get('password'),
                password_salt=
            )
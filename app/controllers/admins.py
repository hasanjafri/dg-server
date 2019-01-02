""" Admins controller using Sanic Class based views. """
import datetime

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin
from app.utils.auth import create_password

class AdminController(HTTPMethodView):
    """ Handles Admin CRUD operations. """
    
    async def get(self, request):
        pass
    
    async def post(self, request):
        for param in ['email', 'password', 'firstName', 'lastName', 'phoneNum', 'country', 'countryCode', 'bday', 'tier', 'period']:
            if request.json[param] == "":
                return json({'error': '{} field cannot be blank!'.format(param)}, status=400)
        
        (salt, password) = create_password(request.json.get('password'))
        bday_str = request.json.get('bday').split('-')
        bday = datetime.date(int(bday_str[0]), int(bday_str[1]), int(bday_str[2]))

        with scoped_session() as session:
            admin = Admin(
                email=request.json.get('email'),
                password=password,
                password_salt=salt,
                birthday=bday,
                first_name=request.json.get('firstName'),
                last_name=request.json.get('lastName'),
                phone_num=request.json.get('phoneNum'),
                country=request.json.get('country'),
                country_code=request.json.get('countryCode'),
                subscription_tier=request.json.get('tier'),
                subscription_period=request.json.get('period')
            )
            session.add(admin)

        return json({'msg': 'Admin with email: {} was successfully created'.format(request.json.get('email'))})
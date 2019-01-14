""" Admins controller using Sanic Class based views. """
import datetime

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin
from app.utils.auth import create_password

class AdminController(HTTPMethodView):
    """ Handles Admin CRUD operations. """
    
    async def valid_api_key(self, api_key):
        with scoped_session() as session:
            admin = session.query(Admin).filter_by(api_key=api_key).one()
            if admin.is_active == True:
                return True
            else:
                return False
    
    async def post(self, request):
        """ Creates a new admin.
        Args:
            request (object): contains data pertaining request.
        Returns:
            json: containing key `msg` with success info & email.
        """

        for param in ['email', 'password', 'firstName', 'lastName', 'phoneNum', 'country', 'countryCode', 'bday', 'tier', 'period', 'security_answer']:
            if request.json.get(param) == None:
                return json({'error': '{} field cannot be blank!'.format(param)}, status=400)
        
        email = request.json.get('email')
        (salt, password) = create_password(request.json.get('password'))
        bday_str = request.json.get('bday').split('-')
        bday = datetime.date(int(bday_str[0]), int(bday_str[1]), int(bday_str[2]))

        subscription_period = request.json.get('period')
        if subscription_period == '1':
            subscription_end = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        elif subscription_period == '2':
            subscription_end = datetime.datetime.utcnow() + datetime.timedelta(days=365)

        with scoped_session() as session:
            admin = Admin(
                email=email,
                password=password,
                password_salt=salt,
                birthday=bday,
                first_name=request.json.get('firstName'),
                last_name=request.json.get('lastName'),
                phone_num=request.json.get('phoneNum'),
                country=request.json.get('country'),
                country_code=request.json.get('countryCode'),
                subscription_tier=request.json.get('tier'),
                subscription_period=subscription_end,
                security_answer=request.json.get('security_answer')
            )
            session.add(admin)

        return json({'success': 'true'})

    async def delete(self, request):

        email = request.json.get('email')

        with scoped_session() as session:
            session.query(Admin).filter_by(email=email).delete()
            session.commit()
            
        return json({'msg': 'Admin with email {} was successfully deleted'.format(email)})
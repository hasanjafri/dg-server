import datetime

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin
from app.models.users import User
from app.utils.auth import check_password

class SessionAuthController(HTTPMethodView):
    """ Handles session auth operations """

    async def get(self, request):
        if not request['session'].get('DG_api_key'):
            return json({'error': 'Unauthenticated'})
        else:
            api_key = request['session'].get('DG_api_key')
            return json({'success': 'Authenticated'})
                
    async def post(self, request):
        for param in ['username', 'password', 'account_type']:
            if request.json.get(param) == None:
                return json({'error': '{} field cannot be blank'.format(param)}, status=400)

        username = request.json.get('email')
        raw_password = request.json.get('password')
        account_type = request.json.get('account_type')

        user = self.get_user_by_username(account_type, username)
        if user != None:
            if check_password(raw_password.encode('utf-8'), user.password_salt, user.password):
                await self.register_user_login(account_type, username)
                request['session']['DG_api_key'] = user.api_key
                return json({'msg': 'success'})
            else:
                return json({'error': 'Wrong email or password'}, status=401)
        else:
            return json({'error': 'No user found with this username'}, status=400)

    async def get_user_by_username(self, account_type, username):
        if account_type == 'user':
            with scoped_session() as session:
                user = session.query(User).filter_by(user_name=username).one()
        elif account_type == 'admin':
            with scoped_session() as session:
                user = session.query(Admin).filter_by(email=username).one()
        
        return user

    async def register_user_login(self, account_type, username):
        if account_type == 'user':
            with scoped_session() as session:
                session.query(User).filter_by(user_name=username).update({'last_logged_in': datetime.datetime.utcnow()})
                session.commit()
        elif account_type == 'admin':
            with scoped_session() as session:
                session.query(Admin).filter_by(email=username).update({'last_logged_in': datetime.datetime.utcnow()})
                session.commit()

        return
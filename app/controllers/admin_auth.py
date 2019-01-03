import datetime

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin
from app.utils.auth import check_password

class AdminAuthController(HTTPMethodView):
    """ Handles Admin Auth operations. """

    async def get_admin_by_email(self, email):
        with scoped_session() as session:
            admin = session.query(Admin).filter_by(email=email).one()

        return admin

    async def register_admin_login(self, admin):

        with scoped_session() as session:
            session.query(Admin).filter_by(id=admin.id, email=admin.email).update({'last_logged_in': datetime.datetime.utcnow()})
            session.commit()

        return 

    async def get(self, request):
        for param in ['email', 'password']:
            if request.json.get(param) == None:
                return json({'error': '{} field cannot be blank!'.format(param)}, status=400)

        email = request.json.get('email')
        raw_password = request.json.get('password')

        admin = await self.get_admin_by_email(email)

        if check_password(raw_password.encode('utf-8'), admin.password_salt, admin.password):
            await self.register_admin_login(admin)
            return json(admin.to_dict())
        else:
            return json({'error': 'Wrong email or password. Please try again'}, status=401)

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
        if not request['session'].get('DG_api_key'):
            return 
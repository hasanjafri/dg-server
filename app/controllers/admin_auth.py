import datetime

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin

class AdminAuthController(HTTPMethodView):
    """ Handles Admin Auth operations. """

    async def get(self, request):
        for param in ['email', 'password']:
            if request.json.get(param) == None:
                return json({'error': '{} field cannot be blank!'.format(param)}, status=400)

        email = request.json.get('email')
        raw_password = request.json.get('password')

        with scoped_session() as session:

""" Admins controller using Sanic Class based views. """

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.admins import Admin

class AdminController(HTTPMethodView):
    """ Handles Admin CRUD operations. """
    
    async def get(self, request):
        pass
    
    async def post(self, request):
        pass
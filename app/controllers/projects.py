""" Projects controller using Sanic Class based views. """

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.projects import Project

class ProjectController(HTTPMethodView):
    """ Handles Project CRUD operations. """
    
    async def 

    async def get(self, request):
        pass
    
    async def post(self, request):
        pass
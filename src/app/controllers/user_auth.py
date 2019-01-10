import datetime

from sanic.response import json
from sanic.views import HTTPMethodView

from app.database import scoped_session, Session
from app.models.users import User

class UserAuthController(HTTPMethodView):
    """ Handles User Auth operations. """

    
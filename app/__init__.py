""" App entry point. """
import aioredis
import os

from sanic import Sanic
from sanic_cors import CORS
from sanic_session import Session, AIORedisSessionInterface

def create_app():
    """ Function for bootstrapping sanic app. """

    app = Sanic(__name__)
    session = Session()
    CORS(app, automatic_options=True)

    # Register Blueprints/Views.
    from app.controllers.users import UserController
    from app.controllers.admins import AdminController
    from app.controllers.projects import ProjectController

    @app.listener('before_server_start')
    async def server_init(app, loop):
        app.redis = await aioredis.create_redis_pool(os.environ.get('REDIS_URL'))
        session.init_app(app, interface=AIORedisSessionInterface(app.redis))

    app.add_route(UserController.as_view(), '/api/user')
    app.add_route(AdminController.as_view(), '/api/admin')
    app.add_route(ProjectController.as_view(), '/api/project')

    app.go_fast(host='0.0.0.0', port=6969, debug=True)
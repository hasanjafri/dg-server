""" App entry point. """
import aioredis
import os

from sanic import Sanic
from sanic_cors import CORS
from sanic.response import text, json
from sanic_session import Session, AIORedisSessionInterface

def create_app():
    """ Function for bootstrapping sanic app. """

    app = Sanic(__name__)
    session = Session()
    CORS(app, automatic_options=True, supports_credentials=True, origins="http://localhost:3000")

    # Register Blueprints/Views.
    from app.controllers.users import UserController
    from app.controllers.admins import AdminController
    from app.controllers.projects import ProjectController
    from app.controllers.session_auth import SessionAuthController
    from app.controllers.suppliers import SupplierController

    @app.listener('before_server_start')
    async def server_init(app, loop):
        app.redis = await aioredis.create_redis_pool((os.environ["REDIS_HOST"], 6379))
        session.init_app(app, interface=AIORedisSessionInterface(app.redis))

    @app.listener('after_server_stop')
    async def after_server_stop(app, loop):
        app.redis.close()
        await app.redis.wait_closed()

    @app.route('/test')
    async def test_session(request):
        if request['session'].get('DG_api_key'):
            return text('Authenticated')
        else:
            return text('Unauthenticated')             

    @app.route('/set')
    async def set_session(request):
        request['session']['DG_api_key'] = 'hey123'
        return text('hey123')

    app.add_route(UserController.as_view(), '/api/user')
    app.add_route(AdminController.as_view(), '/api/admin')
    app.add_route(ProjectController.as_view(), '/api/project')
    app.add_route(SessionAuthController.as_view(), '/api/auth')
    app.add_route(SupplierController.as_view(), '/api/supplier')

    app.go_fast(host='0.0.0.0', port=6969, debug=True)

if __name__ == "__main__":
    create_app()
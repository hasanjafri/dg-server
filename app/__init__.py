""" App entry point. """
import aioredis
import os

from sanic import Sanic
from sanic_cors import CORS
from sanic.response import text
from sanic_session import Session, AIORedisSessionInterface

from app.scripts.initdb import createDb

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
        app.redis = await aioredis.create_redis_pool(os.environ["REDIS_HOST"])
        session.init_app(app, interface=AIORedisSessionInterface(app.redis))

    @app.listener('after_server_stop')
    async def after_server_stop(app, loop):
        app.redis.close()
        await app.redis.wait_closed()

    @app.route('/test')
    async def test_session(request):
        if not request['session'].get('DG_api_key'):
            request['session']['DG_api_key'] = 0

        print(request['session'].get('DG_api_key'))
        request['session']['DG_api_key'] += 1

        response = text(request['session']['DG_api_key'])

        return response

    app.add_route(UserController.as_view(), '/api/user')
    app.add_route(AdminController.as_view(), '/api/admin')
    app.add_route(ProjectController.as_view(), '/api/project')

    app.go_fast(host='0.0.0.0', port=6969, debug=True)

if __name__ == "__main__":
    createDb()
    create_app()
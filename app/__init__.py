""" App entry point. """
import os
from sanic import Sanic


def create_app():
    """ Function for bootstrapping sanic app. """

    app = Sanic(__name__)

    # Register Blueprints/Views.
    from app.controllers.users import UserController
    from app.controllers.admins import AdminController
    from app.controllers.projects import ProjectController

    app.add_route(UserController.as_view(), '/api/user')
    app.add_route(AdminController.as_view(), '/api/admin')
    app.add_route(ProjectController.as_view(), '/api/project')

    app.go_fast(host='0.0.0.0', port=6969, debug=True)
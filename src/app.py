"""
File that holds the function that creates the app object
"""

import datetime
from inspect import getsourcefile
import os
import sys

from flask import Flask

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
root_dir = os.path.join(current_dir, os.pardir)
sys.path.append(root_dir)


def create_app():

    from src import database
    from src.routes.views import view
    from src.routes.admin.views import admin_view

    app = Flask(__name__)

    app.register_blueprint(view)
    app.register_blueprint(admin_view)

    app.config["SECRET_KEY"] = "verysecretkey"
    app.config["SQLALCHEMY_DATABASE_URI"] = database.uri_string
    app.config["ERROR_404_HELP"] = False

    app.debug = True

    return app


def start_app():
    """
    Starts the app, binding to all hosts.
    """
    app = create_app()
    app.run(host="0.0.0.0")  # host='0.0.0.0' for pord


if __name__ == "__main__":
    start_app()

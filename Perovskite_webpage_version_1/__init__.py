"""
The flask application package.
"""

from flask import Flask
from .views import init_app


def create_app():

    app = Flask(__name__)
    init_app(app)

    return app

from flask import Flask
from flask_restful import Api
from ../db import db_session

from ProbeConfig import ProbeConfig




def create_app():
  """Initialize the core application."""
  app = Flask(__name__)
  api = Api(app, catch_all_404s=True)

  @app.teardown_appcontext
  def shutdown_session(exception=None):
    db_session.remove()

  api.add_resource(ProbeConfig)
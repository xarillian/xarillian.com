from flask import Flask

from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    with app.app_context():
        from . import routes  # pylint: disable=C0415
        app.register_blueprint(routes.main)

    return app

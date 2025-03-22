from flask import Flask, render_template

from config import Config


def create_app():
  app = Flask(__name__, static_folder='static', static_url_path='/')
  app.config.from_object(Config)

  @app.after_request
  def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

  with app.app_context():
    from . import routes  # pylint: disable=C0415
    app.register_blueprint(routes.main)
    app.jinja_env.globals['config'] = app.config

    @app.errorhandler(404)
    def page_not_found():
      return render_template('404.html'), 404

  return app

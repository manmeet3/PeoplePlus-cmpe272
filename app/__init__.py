# app/__init__.py
import os
# third-party imports
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_oidc import OpenIDConnect
# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()
#login_manager = LoginManager()
# db object which we will use to interact with the database.
oidc = OpenIDConnect()


# create_app functiongiven a configuration name, loads the correct
# configuration from the config.py file, as well as the configurations
# from the instance/config.py file.
def create_app(config_name):
    if os.getenv('FLASK_CONFIG') == "production":
        app = Flask(__name__)
        app.config.update(
            SECRET_KEY=os.getenv('SECRET_KEY'),
            SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI'),
        )
    else:    
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_object(app_config[config_name])
        app.config.from_pyfile('config.py')
        app.config.update({
        'TESTING': True,
        'DEBUG': True,
        'OIDC_CLIENT_SECRETS': 'client_secrets.json',
        'OIDC_ID_TOKEN_COOKIE_SECURE': False,
        'OIDC_REQUIRE_VERIFIED_EMAIL': False,
        'OIDC_VALID_ISSUERS': ['http://localhost:8080/auth/realms/BlueHats'],
        'OIDC_OPENID_REALM': 'http://localhost:5000'
        })
    Bootstrap(app)
    db.init_app(app)
    oidc.init_app(app)
    #migrate = Migrate(app, db)

    from app import models

    from .hr import hr as hr_blueprint
    app.register_blueprint(hr_blueprint, url_prefix='/hr')

    from .manager import manager as manager_blueprint
    app.register_blueprint(manager_blueprint, url_prefix='/manager')

    from .employee import employee as employee_blueprint
    app.register_blueprint(employee_blueprint, url_prefix='/employee')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    return app

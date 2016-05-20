from flask import Flask

# from flask.ext.bootstrap import Bootstrap
# from flask.ext.mail import Mail
# from flask.ext.moment import Moment
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_debugtoolbar import DebugToolbarExtension

from config import config

from .change_cdn import change_cdn
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
# toolbar = DebugToolbarExtension()

login_manager = LoginManager()

# Mountqi: 暂时把强保护关闭了
# login_manager.session_protection = 'strong'
login_manager.session_protection = 'basic'
login_manager.login_view = "auth.login"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    change_cdn(app)

    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    # toolbar.init_app(app)

    # if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
    #     from flask.ext.sslify import SSLify
    #     sslify = SSLify(app)
    #
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .customer import customer as customer_blueprint
    app.register_blueprint(customer_blueprint)

    from .experiment import experiment as experiment_blueprint
    app.register_blueprint(experiment_blueprint)

    return app

def check_empty( data ):
    if not data:
        return ""
    else:
        return str(data)
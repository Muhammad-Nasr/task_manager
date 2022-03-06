from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from main.config import Config


db = SQLAlchemy()

# config bcrypt
bcrypt = Bcrypt()

# config login
login_manager = LoginManager()
login_manager.login_view = 'users.login_page'

mail = Mail()


# create a configuration function for creating many apps


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from main.users.routes import users
    from main.tasks.routes import tasks
    from main.home.routes import home
    from main.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(tasks)
    app.register_blueprint(home)
    app.register_blueprint(errors)

    return app

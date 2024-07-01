from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager(app)
    login_manager.login_view = 'user_login'

    admin_login_manager = LoginManager(app)
    admin_login_manager.login_view = 'admin_login'

    from .models import User, Admin

    @login_manager.user_loader
    def load_user(user_id):
        """
        Load a user from the database by ID for regular user authentication.

        Args:
            user_id (int): The ID of the user to load.

        Returns:
            User: The User object corresponding to the given ID.
        """
        return User.query.get(int(user_id))
    
    @admin_login_manager.user_loader
    def load_admin(admin_id):
        return Admin.query.get(int(admin_id))

    with app.app_context():
        from . import models
        db.create_all()

    from .routes import main
    app.register_blueprint(main)

    return app

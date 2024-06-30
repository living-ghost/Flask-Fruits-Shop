"""
Application Setup for the Flask Fruits Shop

This module initializes the Flask application, sets up the configuration, 
and integrates essential components such as SQLAlchemy, Flask-Migrate, 
and Flask-Login. It also registers the main blueprint for the application.

Components:
- `db`: SQLAlchemy instance for database management.
- `migrate`: Flask-Migrate instance for handling database migrations.
- `create_app(config_name)`: Function to create and configure the Flask application.

Configuration:
- The application configuration is loaded based on the `config_name` argument.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from .config import config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    """
    Create and configure the Flask application.

    This function initializes the Flask application with configuration settings,
    sets up SQLAlchemy for database interactions, configures Flask-Migrate for 
    database migrations, and sets up Flask-Login for user authentication.
    It also defines the user loaders for both regular users and admin users 
    and registers the main blueprint for routing.

    Args:
        config_name (str): The name of the configuration to use. This should correspond
                           to a key in the `config` dictionary imported from the `config` module.

    Returns:
        Flask: The configured Flask application instance.

    Components:
        - `app`: The Flask application instance.
        - `db`: The SQLAlchemy instance for ORM and database interactions.
        - `migrate`: The Flask-Migrate instance for database migration management.
        - `login_manager`: The Flask-Login instance configured for user authentication.
        - `admin_login_manager`: Another instance of Flask-Login configured for admin authentication.
        - `main`: The main blueprint for the application, imported and registered with the app.

    Application Context:
        - Calls `db.create_all()` to create all tables defined in the models within the application context.

    Configuration:
        - The configuration is loaded from the `config` object based on the provided `config_name`.
        - `login_manager.login_view` is set to `'user_login'` for regular user authentication.
        - `admin_login_manager.login_view` is set to `'admin_login'` for admin authentication.

    Usage:
        - This function is typically called in the application's entry point to initialize the app.
        - Example:
            ```python
            app = create_app('development')
            ```

    Example:
        >>> from app import create_app
        >>> app = create_app('development')
    """
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
        """
        Load an admin from the database by ID for admin authentication.

        Args:
            admin_id (int): The ID of the admin to load.

        Returns:
            Admin: The Admin object corresponding to the given ID.
        """
        return Admin.query.get(int(admin_id))

    with app.app_context():
        from . import models
        db.create_all()

    from .routes import main
    app.register_blueprint(main)

    return app

"""
Configuration Settings for Flask Fruits Shop

This module defines various configuration classes for different environments 
in the Flask application. It provides the configuration for the application 
based on the environment (`development`, `testing`, or `production`). 

Classes:
- `Config`: Base configuration class with default settings.
- `DevConfig`: Configuration for the development environment with debugging enabled.
- `TestConfig`: Configuration for the testing environment with debugging enabled.
- `ProdConfig`: Configuration for the production environment with debugging disabled.

`config` Dictionary:
- A dictionary mapping environment names to their respective configuration classes.

Configuration Settings:
- `SECRET_KEY`: Secret key for session management and cryptographic operations.
- `SQLALCHEMY_DATABASE_URI`: URI for connecting to the database.
- `UPLOAD_FOLDER`: Directory path for file uploads.
- `SQLALCHEMY_TRACK_MODIFICATIONS`: Flag to disable SQLAlchemy event system to save memory.
- `DEBUG`: Flag to enable or disable debugging mode.
"""

import os

class Config:
    """
    Base configuration class for the Flask application.

    This class contains common settings and default values used across 
    different environments. Subclasses can inherit from this class and 
    override specific attributes as needed.

    Attributes:
        SECRET_KEY (str): Secret key for session management and cryptographic operations.
        SQLALCHEMY_DATABASE_URI (str): URI for connecting to the database.
        UPLOAD_FOLDER (str): Directory path for file uploads.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disable Flask-SQLAlchemy's event system to save memory.
        DEBUG (bool): Flag to enable or disable debugging mode.

    Default Settings:
        - `SECRET_KEY`: Fallback to 'abcdefghijk' if environment variable is not set.
        - `SQLALCHEMY_DATABASE_URI`: Fallback to 'sqlite:///sample.db' if environment variable is not set.
        - `UPLOAD_FOLDER`: 'static/uploads' directory for file uploads.
        - `SQLALCHEMY_TRACK_MODIFICATIONS`: Disabled (set to `False`).
        - `DEBUG`: Disabled (set to `False`).
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abcdefghijk'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///sample.db'
    UPLOAD_FOLDER = 'static/uploads'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False


class DevConfig(Config):
    """
    Configuration for the development environment.

    Inherits from `Config` and overrides specific settings for the development environment.

    Attributes:
        DEBUG (bool): Enabled (set to `True`) for debugging purposes.
    """
    DEBUG = True
    

class TestConfig(Config):
    """
    Configuration for the testing environment.

    Inherits from `Config` and overrides specific settings for the testing environment.

    Attributes:
        DEBUG (bool): Enabled (set to `True`) for debugging purposes.
    """
    DEBUG = True


class ProdConfig(Config):
    """
    Configuration for the production environment.

    Inherits from `Config` and overrides specific settings for the production environment.

    Attributes:
        DEBUG (bool): Disabled (set to `False`) for production environments.
    """
    DEBUG = False


config = {
    """
    Dictionary mapping environment names to their respective configuration classes.

    This dictionary allows the application to load the appropriate configuration 
    class based on the environment specified.

    Keys:
        'development': `DevConfig` - Configuration for the development environment.
        'testing': `TestConfig` - Configuration for the testing environment.
        'production': `ProdConfig` - Configuration for the production environment.
        'default': `DevConfig` - Default configuration used if no environment is specified.

    Usage:
        - The `config_name` argument in the `create_app` function selects the appropriate class.
        - Example:
            ```python
            app = create_app('development')  # Loads DevConfig
            ```
    """
    'development': DevConfig,
    'testing': TestConfig,
    'production': ProdConfig,
    'default': DevConfig
}

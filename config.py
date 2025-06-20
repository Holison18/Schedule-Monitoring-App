import os

# This line gets the absolute path to the directory where this config.py file lives.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-very-secret-key'

    # This creates a full, unambiguous path to your database file.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'site.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
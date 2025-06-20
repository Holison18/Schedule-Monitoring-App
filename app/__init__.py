import os
from flask import Flask
from datetime import datetime
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure the instance folder exists as defined by app.instance_path.
    # For an app structure like 'project_root/app_package/', app.instance_path
    # typically points to 'project_root/instance/'.
    # The default config SQLALCHEMY_DATABASE_URI='sqlite:///instance/site.db'
    # relies on the CWD being 'project_root/' (in this case, 'monitoring_schedule/')
    # for the path to resolve correctly to 'project_root/instance/site.db'.
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import Pair
    @login_manager.user_loader
    def load_user(user_id):
        return Pair.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/')

    from .dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')
    
    # Add a context processor to make the current year available in all templates
    @app.context_processor
    def inject_current_year():
        return {'current_year': datetime.utcnow().year}

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # db.create_all() is only for initial creation, migrations handle updates
    with app.app_context(): # Consider removing this line after first migration
        db.create_all()

    return app
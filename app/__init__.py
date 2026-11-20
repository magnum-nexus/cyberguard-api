from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models agar terdeteksi oleh Flask-Migrate
    from app.models import cyber_models

    # Daftarkan global error handlers
    from app.utils.error_handlers import register_error_handlers
    register_error_handlers(app)

    # Daftarkan Blueprint Routes API v1
    from app.routes.api_routes import api_bp
    app.register_blueprint(api_bp)

    return app
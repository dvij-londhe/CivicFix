from flask import Flask
from app.db import get_connection

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'My_Secret_Key'

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'CivicFix'
    app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 5}

    from app.routes.main_routes import main
    from app.routes.auth import auth
    from app.routes.user_routes import user_bp
    from app.routes.complaint_routes import complaint
    from app.routes.notification_routes import notification
    from app.routes.admin_routes import admin

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(user_bp)
    app.register_blueprint(complaint)
    app.register_blueprint(notification)
    app.register_blueprint(admin)

    return app
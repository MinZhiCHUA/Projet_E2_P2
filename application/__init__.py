from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .extension import db
from flask_login import LoginManager

# db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///..//db2.db'
    #from .models import db
    # from . import db
    db.init_app(app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
        
    # blueprint for auth routes in our app
    from .user_routes import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .nonuser_routes import main as main_blueprint
    app.register_blueprint(main_blueprint)


    # from application.user_routes import simple_page
    # app.register_blueprint(simple_page)
    return app
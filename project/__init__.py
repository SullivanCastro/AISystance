from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from flask_login import LoginManager, current_user

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Configure the database
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # setup Flask-Security
    from .models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore=user_datastore)
    security_bp = security.init_app(app)

    # Initialise the app
    db.init_app(app)

    # Initialise the login system
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Define the user retrieval method for Flask-Security
    @security_bp.context_processor
    def security_context_processor():
        return dict(
            user=current_user if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated else None,
            has_role=user_datastore.has_role if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated else None

        )

    # Define the user retrieval method for login system
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(user_id)

    # Create all tables
    with app.app_context():
        # uncomment if you want to reset the database
        # db.drop_all()
        db.create_all()
        data_role = Role(name='data')
        admin_role = Role(name='admin')
        db.session.add(data_role)
        db.session.add(admin_role)
        db.session.commit()

    # Blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

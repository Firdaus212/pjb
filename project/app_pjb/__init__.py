from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed
import matlab.engine

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

# init MATLAb Engine
future = matlab.engine.start_matlab(background=True)
eng = future.result()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder='static')

    app.config['SECRET_KEY'] = 'secretPJB'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    principal = Principal(app)
    principal.init_app (app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    @ identity_loaded.connect_via(app)
    def on_identity_loaded (sender, identity):
        identity.user=current_user
        if hasattr (current_user, "id"):
            identity.provides.add (UserNeed (current_user.id))
        if hasattr (current_user, "role"):
            identity.provides.add (RoleNeed (current_user.role))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

     # blueprint for non-auth parts of app
    from .opt_data import opt_data as opt_data_blueprint
    app.register_blueprint(opt_data_blueprint, url_prefix='/opt-data')

    return app
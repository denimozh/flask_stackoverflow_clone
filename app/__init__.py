from flask import Flask, flash
from app.config import Config
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

login_manager = LoginManager(app)

login_manager.login_view = 'login'

login_manager.login_message = 'Please log in'

from app.models import like, user, answer, question, answerLike

migrate = Migrate(app, db)

migrate.init_app(app, db)

from app.controllers import auth_controller, home_controller

if __name__ == "__main__":
    app.run(debug=True)
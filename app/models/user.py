from app import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(20), nullable = False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    points = db.Column(db.Integer(), default=0)
    level = db.Column(db.Integer(), default=0)
    rank = db.Column(db.Integer(), default=0)
    isAdmin = db.Column(db.Boolean(), default=False)

    questions = db.relationship("Question", backref="questionAuthor", lazy="dynamic")
    answers = db.relationship("Answer", backref="answerAuthor", lazy="dynamic")

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
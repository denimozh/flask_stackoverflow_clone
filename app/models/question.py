from datetime import datetime
from app import db
from app.models.like import user_questions, user_questions_dislike

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), index=True)
    body = db.Column(db.Text(), index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    close = db.Column(db.Boolean, default = False)
    likes = db.Column(db.Integer, default = 0)
    dislikes = db.Column(db.Integer, default = 0)

    users_liked = db.relationship('User', secondary=user_questions, backref="liked_questions")
    users_dislikes = db.relationship('User', secondary=user_questions_dislike, backref="disliked_questions")
    answers = db.relationship("Answer", backref="question", lazy="dynamic")

    def __repr__(self):
        return 'Question {}'.format(self.body)
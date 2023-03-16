from datetime import datetime
from app import db
from app.models.answerLike import user_answers, user_answers_dislike

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text(), index=True)
    like = db.Column(db.Integer, default=0)
    dislike = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    users_liked = db.relationship('User', secondary=user_answers, backref="liked_answers")
    users_dislikes = db.relationship('User', secondary=user_answers_dislike, backref="disliked_answers")

    def __repr__(self):
        return 'Answer {}'.format(self.body)
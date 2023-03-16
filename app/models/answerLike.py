from app import db

user_answers = db.Table('user_answers',
                          db.Column('answers_id', db.Integer, db.ForeignKey('answer.id')),
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                          )

user_answers_dislike = db.Table('user_answer_dislike',
                                  db.Column('answers_id', db.Integer, db.ForeignKey('answer.id')),
                                  db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                                 )
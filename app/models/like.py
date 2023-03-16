from app import db

user_questions = db.Table('user_questions',
                          db.Column('questions_id', db.Integer, db.ForeignKey('question.id')),
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                          )

user_questions_dislike = db.Table('user_question_dislike',
                                  db.Column('questions_id', db.Integer, db.ForeignKey('question.id')),
                                  db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
                                 )
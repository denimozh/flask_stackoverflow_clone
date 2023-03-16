from app import app, db
from flask import render_template, redirect, url_for, request
from app.forms.question_form import QuestionForm
from app.models.question import Question
from app.models.answer import Answer
from app.forms.answer_form import AnswerForm
from flask_login import current_user, login_required

@app.route('/')
@app.route('/home/')

def home():
    lastQuestions = db.session.query(Question).order_by(db.desc(Question.timestamp)).limit(5)

    return render_template(
        "home/home.html",
        questions=lastQuestions
    )

@app.route('/addquestion', methods=['post', 'get'])
@login_required
def addQuestion():
    form = QuestionForm()
    if form.validate_on_submit():
        headerQuestion = form.title.data
        bodyQuestion = form.body.data
        quest = Question(title = headerQuestion, body = bodyQuestion, user_id = current_user.id)
        print(quest)
        db.session.add(quest)
        db.session.commit()
    return render_template('home/question.html', form=form)

@app.route("/edit/<int:question_id>", methods=['post', 'get'])
@login_required
def editQuestion(question_id):
    question = Question.query.get(question_id)
    form = QuestionForm()
    if form.validate_on_submit():
        question.title = form.title.data
        question.body = form.body.data
        db.session.commit()
        return redirect(url_for('answers', question_id=question.id))
    elif request.method == "GET":
        form.title.data = question.title
        form.body.data = question.body

    return render_template("home/question.html", form=form)

@app.route('/like/<int:question_id>')
@login_required
def likedQuestion(question_id):
    question = Question.query.get(question_id)
    if question not in current_user.liked_questions:
        question.likes += 1
        current_user.liked_questions.append(question)
        if question in current_user.disliked_questions:
             question.dislikes -= 1
             current_user.disliked_questions.remove(question)
        db.session.commit()

    return redirect("/")

@app.route('/dislike/<int:question_id>')
@login_required
def dislikedQustion(question_id):
     question = Question.query.get(question_id)
     if question not in current_user.disliked_questions:
         question.dislikes += 1
         current_user.disliked_questions.append(question)
         if question in current_user.liked_questions:
             question.likes -= 1
             current_user.liked_questions.remove(question)
         db.session.commit()

     return redirect("/")

@app.route('/unlike/<int:question_id>')
@login_required
def unlikedQuestion(question_id):
    question = Question.query.get(question_id)
    if question in current_user.liked_questions:
        question.likes -= 1
        current_user.liked_questions.remove(question)

        db.session.commit()

    return redirect("/")

@app.route('/undislike/<int:question_id>')
@login_required
def undislikedQuestion(question_id):
    question = Question.query.get(question_id)
    if question in current_user.disliked_questions:
        question.dislikes -= 1
        current_user.disliked_questions.remove(question)

        db.session.commit()

    return redirect("/")

@app.route('/deletequestion/<int:question_id>')
@login_required
def deleteQuestion(question_id):
    question = Question.query.get(question_id)
    if question.user_id == current_user.id:
        db.session.delete(question)
        db.session.commit()
    return redirect("/")

@app.route('/answers/<int:question_id>', methods=['post', 'get'])
def answers(question_id):
    question = Question.query.get(question_id)
    sortedAnswers = db.session.query(Answer).filter(Answer.question_id == question_id).order_by(db.desc(Answer.like)).all()
    form = AnswerForm()
    if current_user.is_authenticated and form.validate_on_submit():
        bodyQuestion = form.body.data
        ans = Answer(body = bodyQuestion, user_id = current_user.id, like = 0, dislike = 0, question_id = question_id)
        print(ans)
        db.session.add(ans)
        db.session.commit()
        return redirect(url_for('answers', question_id=question_id))

    return render_template('answers/answers.html', form=form, question=question, sorted_answers=sortedAnswers)

@app.route('/delete_answer/<int:answer_id>')
@login_required
def deleteAnswer(answer_id):
    answer = Answer.query.get(answer_id)
    if answer.user_id == current_user.id:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('answers', question_id=answer.question_id))

@app.route('/answerlike/<int:answer_id>')
@login_required
def likedAnswer(answer_id):
    answer = Answer.query.get(answer_id)
    if answer not in current_user.liked_answers:
        answer.like += 1
        current_user.liked_answers.append(answer)
        if answer in current_user.disliked_answers:
             answer.dislike -= 1
             current_user.disliked_answers.remove(answer)
        db.session.commit()

    return redirect(f"/answers/{answer.question_id}")

@app.route('/answerdislike/<int:answer_id>')
@login_required
def dislikedAnswer(answer_id):
     answer = Answer.query.get(answer_id)
     if answer not in current_user.disliked_answers:
         answer.dislike += 1
         current_user.disliked_answers.append(answer)
         if answer in current_user.liked_answers:
             answer.like -= 1
             current_user.liked_answers.remove(answer)
         db.session.commit()

     return redirect(f"/answers/{answer.question_id}")

if __name__ == "__main__":
    app.run(debug=True)
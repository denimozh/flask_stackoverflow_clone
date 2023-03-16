from app import app, db
from flask_login import login_required, logout_user, LoginManager, current_user, login_user
from flask import render_template, redirect, url_for, flash

from app.forms.registration_form import RegistrationForm
from app.forms.login_form import LoginForm

from app.models.user import User

@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You entered into the system!')
        return redirect(url_for('login'))
    return render_template('auth/registration.html', title='Регистрация', form=form)

@app.route('/login/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))

        flash("Incorrect Password or Username", "Error")
        return redirect(url_for('login'))
    return render_template('auth/login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You exited the system.")
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    return render_template('auth/profile.html')
from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db, app
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm, SetPasswordForm, ResetPasswordForm
from app.models import User
from database import add_user_to_database
from app.email import send_email


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        result = add_user_to_database(user, db.users)
        flash('You are now registered')
        send_email('Welcome!',
                   sender=app.config['ADMINS'][0],
                   recipients=[user.email],
                   text_body=render_template('email/welcome.txt',
                                             user=user),
                   html_body=render_template('email/welcome.html',
                                             user=user)
                   )
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_from_db = db.users.find_one({"email": form.email.data})
        if user_from_db is not None:
            user = User(id=user_from_db['_id'], email=user_from_db['email'],
                        password_hash=user_from_db['password_hash'], favorites=user_from_db['favorites'])
        else:
            user = None
        flash('Login requested for {}, remember {}'.format(form.email.data, form.remember_me.data))
        if user is None:
            flash('Email not recognized')
            return redirect(url_for('auth.login'))
        elif not user.check_password(form.password.data):
            flash('Incorrect password')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        redirect_page = request.args.get('next')
        if not redirect_page or url_parse(redirect_page).netloc != '':  # 2nd condition prevents redirect to diff site
            redirect_page = url_for('index')
        return redirect(redirect_page)

    return render_template('auth/login.html', title='Log in', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated: # should never reach due to dynamically showing logout/ login
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user_from_db = db.users.find_one({"email": form.email.data})
        if user_from_db:
            user_ = User(id=user_from_db['_id'], email=user_from_db['email'],
                        password_hash=user_from_db['password_hash'], favorites=user_from_db['favorites'])
            reset_token = user_.get_reset_password_token()
            send_email('Reset Your Password',
                       sender=app.config['ADMINS'][0],
                       recipients=[user_.email],
                       text_body=render_template('email/reset_password.txt',
                                                 user=user_, token=reset_token),
                       html_body=render_template('email/reset_password.html',
                                                 user=user_, token=reset_token)
                       )
            flash('Check your email for reset instructions')
            return redirect(url_for('auth.login'))
        else:
            flash('Email not recognized, please try again')

    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)


@bp.route('/reset_passowrd/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:  # should never reach due to dynamically showing logout/ login
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = SetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        result = add_user_to_database(user, db.users)
        flash('You have successfully reset your password! Please login')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

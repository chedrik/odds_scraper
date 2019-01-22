from flask import render_template, flash, redirect, url_for, request, current_app, abort
from flask_login import current_user, login_required
from app import db
from app.main.forms import DeleteAccountForm, ConfirmForm
from app.models import User
from app.email import send_email
from app.models import delete_user
from app.main import bp
from database import get_games_by_sport


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')


@bp.route('/user/')  # TODO: proper fix for 404 error on /user/ despite login_required
@bp.route('/user/<email>', methods=['GET', 'POST'])
@login_required
def user(email=None):
    if email is None:
        email = current_user.email
    user_from_db = db.users.find_one({"email": email})
    if user_from_db is None:
        abort(404)
    user_ = User(id=user_from_db['_id'], email=user_from_db['email'],
                 password_hash=user_from_db['password_hash'], favorites=user_from_db['favorites'])
    games, gameless_favorites = user_.get_all_favorites()
    # TODO: pagination?

    if request.method == 'POST':
        if request.form.get('favorites'):
            if request.form['favorites'] in current_app.config['FAVORITES']:
                _, not_added = user_.add_favorite([request.form['favorites']])
                if not_added:
                    flash(request.form['favorites'] + ' was already included in your favorites')
                else:
                    flash('Added ' + request.form['favorites'] + ' to favorites')
            else:
                flash('Invalid Selection')
        else:
            if request.form.get('remove_favorites') in current_user.favorites_list:
                result = user_.remove_favorites([request.form.get('remove_favorites')])
                flash('Removed ' + request.form['remove_favorites'] + ' from favorites')
            else:
                flash('Invalid Selection')

        return redirect(url_for('main.user', email=current_user.email))

    return render_template('user.html', user=user_, games=games, gameless_fav=gameless_favorites,
                           cur_fav=current_user.favorites_list,  mylist=current_app.config['FAVORITES'])


@bp.route('/sport/<cur_sport>', methods=['GET', 'POST'])
def sport(cur_sport=None):
    if cur_sport not in current_app.config['SUPPORTED_SPORTS']:
        abort(404)
    games = get_games_by_sport(db, cur_sport)
    return render_template('sport.html', cur_sport=cur_sport, games=games)


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = DeleteAccountForm()
    confirm_form = ConfirmForm()
    if confirm_form.yes.data:
        send_email('Account Deleted',
                   sender=current_app.config['ADMINS'][0],
                   recipients=[current_user.email],
                   text_body=render_template('email/delete_account.txt',
                                             user=current_user),
                   html_body=render_template('email/delete_account.html',
                                             user=current_user)
                   )
        result = delete_user(current_user.id)
        flash('User ' + current_user.email + ' successfully removed')
        return redirect(url_for('main.index'))
    elif confirm_form.no.data:
        return render_template('settings.html', form=form)
    if form.validate_on_submit():
        return render_template('settings.html', form=form, confirm_form=confirm_form)
    return render_template('settings.html', form=form)

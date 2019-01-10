from flask_wtf import FlaskForm
from wtforms import SubmitField


class ConfirmForm(FlaskForm):
    yes = SubmitField('YES')
    no = SubmitField('NO')


class DeleteAccountForm(FlaskForm):
    delete = SubmitField('Delete')

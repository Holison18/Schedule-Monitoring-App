from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField, TextAreaField, DateField
from wtforms.validators import DataRequired, Email, Optional

class LoginForm(FlaskForm):
    pair = SelectField('Select Pair', coerce=int, validators=[DataRequired()])
    email = PasswordField('Email as Password', validators=[DataRequired(), Email()])
    submit = SubmitField('Login')

class ScheduleForm(FlaskForm):
    contacted_school = BooleanField('Have you contacted the school?')
    reason_if_not_contacted = TextAreaField('Reason if not contacted')
    school_unavailable = BooleanField('Is the school unavailable?')
    reason_if_unavailable = TextAreaField('Reason if school is unavailable')
    headmaster_name_on_schedule = StringField('Name of Headmaster', validators=[Optional()])
    headmaster_contact_on_schedule = StringField('Contact of Headmaster', validators=[Optional()])
    scheduled_date = DateField('Select a date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Submit Schedule')
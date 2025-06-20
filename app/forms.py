from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField, TextAreaField, DateField, RadioField
from wtforms.validators import DataRequired, Email, Optional
from datetime import date

class LoginForm(FlaskForm):
    pair = SelectField('Select Pair', coerce=int, validators=[DataRequired()])
    email = PasswordField('Email as Password', validators=[DataRequired(), Email()])
    submit = SubmitField('Login')

class ScheduleForm(FlaskForm):
    contacted_school = RadioField(
        'Have you contacted the school?',
        choices=[('yes', 'Yes'), ('no', 'No')],
        validators=[DataRequired()]
    )
    reason_if_not_contacted = TextAreaField('Reason if not contacted')
    school_unavailable = BooleanField('Is the school unavailable?')
    reason_if_unavailable = TextAreaField('Reason if school is unavailable')
    headmaster_name_on_schedule = StringField('Name of Headmaster', validators=[DataRequired()])
    headmaster_contact_on_schedule = StringField('Contact of Headmaster', validators=[DataRequired()])
    scheduled_date = DateField('Select a date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Submit Schedule')
   
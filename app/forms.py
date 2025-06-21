from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, TextAreaField, DateField, RadioField, BooleanField
from wtforms.validators import DataRequired, Email, Optional
from datetime import date

class LoginForm(FlaskForm):
    pair = SelectField('Select Pair', coerce=int, validators=[DataRequired()])
    email = PasswordField('Email as Password', validators=[DataRequired(), Email()])
    submit = SubmitField('Login')

class ScheduleForm(FlaskForm):
    contacted_school = BooleanField('School Contacted')
    headmaster_name_on_schedule = StringField('Headmaster Name', validators=[Optional()])
    headmaster_contact_on_schedule = StringField('Headmaster Contact', validators=[Optional()])
    scheduled_date = DateField('Scheduled Date', format='%Y-%m-%d', validators=[Optional()])
    reason_if_not_contacted = TextAreaField('Reason if Not Contacted', validators=[Optional()])
    submit = SubmitField('Submit Schedule')

    def validate(self, extra_validators=None):
        # Call the parent class's validate() method, passing extra_validators
        if not super().validate(extra_validators=extra_validators):
            return False

        # Custom validation logic
        if self.contacted_school.data:
            if not self.headmaster_name_on_schedule.data:
                self.headmaster_name_on_schedule.errors.append('This field is required when the school is contacted.')
                return False
            if not self.headmaster_contact_on_schedule.data:
                self.headmaster_contact_on_schedule.errors.append('This field is required when the school is contacted.')
                return False
            if not self.scheduled_date.data:
                self.scheduled_date.errors.append('This field is required when the school is contacted.')
                return False
        else:
            if not self.reason_if_not_contacted.data:
                self.reason_if_not_contacted.errors.append('This field is required when the school is not contacted.')
                return False

        return True
    
    
class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

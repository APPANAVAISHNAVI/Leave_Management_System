from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('employee', 'Employee'), ('manager', 'Manager')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class LeaveForm(FlaskForm):
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    reason = TextAreaField('Reason', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Apply')


class AdminActionForm(FlaskForm):
    admin_comment = TextAreaField('Comment (optional)')
    submit_approve = SubmitField('Approve')
    submit_reject = SubmitField('Reject')
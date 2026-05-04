from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange, Optional


class LoginForm(FlaskForm):
    """Form for user login."""
    email    = StringField('Email address',
                           validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    submit   = SubmitField('Log in')

    def validate_email(self, email):
        """Custom validator: only allow UWA student emails."""
        if not email.data.endswith('@student.uwa.edu.au'):
            raise ValidationError('Please use your UWA student email address.')


class RegisterForm(FlaskForm):
    """Form for new user registration."""
    name     = StringField('Full name',
                           validators=[DataRequired(), Length(min=2, max=80)])
    email    = StringField('Email address',
                           validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6)])
    confirm  = PasswordField('Confirm password',
                             validators=[DataRequired(),
                                         EqualTo('password',
                                                 message='Passwords must match.')])
    submit   = SubmitField('Create account')

    def validate_email(self, email):
        """Custom validator: only allow UWA student emails."""
        if not email.data.endswith('@student.uwa.edu.au'):
            raise ValidationError('Please use your UWA student email address.')


from wtforms import IntegerField, TextAreaField
from wtforms.validators import NumberRange, Optional

class ReviewForm(FlaskForm):
    """Form for submitting or editing a unit review."""

    overall_rating    = IntegerField('Overall rating',
                                     validators=[
                                         DataRequired(),
                                         NumberRange(min=1, max=5, message='Rating must be between 1 and 5.')
                                     ])
    workload_rating   = IntegerField('Workload rating',
                                     validators=[
                                         DataRequired(),
                                         NumberRange(min=1, max=5, message='Rating must be between 1 and 5.')
                                     ])
    difficulty_rating = IntegerField('Difficulty rating',
                                     validators=[
                                         DataRequired(),
                                         NumberRange(min=1, max=5, message='Rating must be between 1 and 5.')
                                     ])
    usefulness_rating = IntegerField('Usefulness rating',
                                     validators=[
                                         DataRequired(),
                                         NumberRange(min=1, max=5, message='Rating must be between 1 and 5.')
                                     ])
    comment           = TextAreaField('Comment',
                                      validators=[Optional()])
    submit            = SubmitField('Submit review')

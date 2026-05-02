from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


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


class ReviewForm(FlaskForm):
    comment = TextAreaField('Review', validators=[
        DataRequired(),
        Length(min=20, message='Review must be at least 20 characters.')
    ])
    submit = SubmitField('Submit review')

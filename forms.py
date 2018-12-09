from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField,BooleanField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                               Length, EqualTo)

from models import User,UserPreferences


def one_shop_preference_only(form, field):
    if field.data == form.food.data or field.data == form.clothing.data:
        raise ValidationError('you can only select one of food,'
                              'clothing or technology.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(Form):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class PreferenceForm(Form):
    content = TextAreaField("What's up?", validators=[DataRequired()])

    student_discount = BooleanField(
        'student_discount',validators=[
            one_shop_preference_only
        ]


    )
    food = BooleanField(default=False)
    clothing = BooleanField(default=False)
    technology = BooleanField(default=False)

class RegisterForm(Form):
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2)],
        password2=PasswordField(
            'Confirm Password',
            validators=[DataRequired()]))
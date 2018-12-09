from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField,BooleanField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                               Length, EqualTo)

from models import User,UserPreferences


def one_shop_preference_only(form, field):
    if field.data == form.food.data or field.data == form.clothing.data:
        raise ValidationError('you can only select one of food,'
                              'clothing or technology.')

def one_shop_preference_only2(form, field):
    if field.data == form.food.data or field.data == form.tecnology.data:
        raise ValidationError('you can only select one of food,'
                              'clothing or technology.')


def email_exists(form, field):
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(FlaskForm):
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

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class PreferenceForm(FlaskForm):


    student_discount = BooleanField(
        'student_discount',validators=[
            one_shop_preference_only
        ]


    )
    food = BooleanField('food')
    clothing = BooleanField('clothing',validators=[
            one_shop_preference_only
        ])
    technology = BooleanField('technology',validators=[
            one_shop_preference_only
        ])




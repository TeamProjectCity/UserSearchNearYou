import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

DATABASE = SqliteDatabase('userSearch.db')

class User(UserMixin,Model):
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)


    def get_preferences(self):
        return UserPreferences.get(user = self.id)
    @classmethod
    def create_user(cls, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    email=email,
                    password=generate_password_hash(password))
        except IntegrityError:
            raise ValueError("User already exists")



class UserPreferences(Model):
    user = ForeignKeyField(User,
                           related_name='preferences'
                           )
    student_discount = BooleanField(default=False)
    food = BooleanField(default=False)
    clothing = BooleanField(default=False)
    technology = BooleanField(default=False)

    class Meta:
        database = DATABASE


    def generate_search_string(self):
        return_string = ["Student%20Discount",
                         "Student%20Discount,Food",
                         "Student%20Discount,Clothing",
                         "Student%20Discount,Technology",
                         "Food",
                         "Clothing",
                         "Technology",]
        if self.student_discount:
            return return_string[0]
        if self.food:
            if self.student_discount:
                return return_string[1]
            else:
                return return_string[4]
        if self.clothing:
            if self.student_discount:
                return return_string[2]
            else:
                return return_string[5]

        if self.technology:
            if self.student_discount:
                return return_string[3]
            else:
                return return_string[6]

        return ""


def initialize():
    with DATABASE:
        DATABASE.create_tables([User, UserPreferences])





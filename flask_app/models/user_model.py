from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe_model
from flask import flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.recipes = []

    # mike = pass123!
    # jenny = 123pass

    @staticmethod
    def vlaidate_user(user):
        is_valid = True
        query = 'select * from users where email = %(email)s ;'
        results = connectToMySQL('recipes').query_db(query,user)
        if len(user['first_name']) < 1:
            flash('First name must be at least 2 characters')
            is_valid = False
        if len(user['last_name']) < 1:
            flash('Last name mush be at least 2 charaters')
            is_valid = False
        if len(user['email']) >=0 and not EMAIL_REGEX.match(user['email']):
            flash('Invalid email format')
            is_valid = False
        if len(results) >=1:
            flash('email already in file')
            is_valid = False
        if len(user['password']) < 7:
            flash('password must be at least 7 charaters')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash('Passwords do not match')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls,form_data):
        pw_hash = bcrypt.generate_password_hash(form_data['password'])
        print(pw_hash)
        data={
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'email': form_data['email'],
            'password': pw_hash
        }
        query = 'Insert into users(first_name, last_name, email, password) values ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );'
        results = connectToMySQL('recipes').query_db(query,data)
        session['first_name'] = form_data['first_name']
        session['last_name'] = form_data['last_name']
        session['user_id'] = results
        print('session',session)
        return results

    @classmethod
    def get_email(cls,data):
        query = 'select * from users where email = %(email)s ;'
        results = connectToMySQL('recipes').query_db(query,data)
        print(results)
        if len(results) < 1:
            return False
        one_user =cls(results[0])
        print(one_user.password)
        return one_user

    @classmethod
    def get_by_id(cls,data):
        query = 'select * from users where id = %(id)s ;'
        results = connectToMySQL('recipes').query_db(query,data)
        print(results)
        return cls(results[0])

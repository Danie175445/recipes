from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user_model
from flask import flash, session

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.date_made = data['date_made']
        self.recipe = None

    @staticmethod
    def validate(recipe):
        is_valid = True
        if len(recipe['name']) < 2:
            flash('name must be at least 3 characters')
            is_valid = False
        if len(recipe['description']) < 2:
            flash('description must be at least 3 characters')
            is_valid = False
        if len(recipe['instructions']) < 2:
            flash('instructions must be at least 3 characters')
            is_valid = False
        if 'under_30' not in recipe:
            flash('under 30 minutes must be filled')
            is_valid = False
        if len(recipe['date_made']) < 1:
            flash('date_made must be filled out')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls,data):
        query = 'insert into recipes(user_id, name, description, instructions, under_30, date_made) values (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(under_30)s, %(date_made)s );'
        return connectToMySQL('recipes').query_db(query,data)

    @classmethod
    def get_all_recipes(cls):
        query = 'select * from recipes join users on users.id = recipes.user_id;'
        results = connectToMySQL('recipes').query_db(query)
        print(results)
        return results

    @classmethod
    def get_recipe(cls,data):
        query = 'select * from recipes where id = %(id)s ;'
        results = connectToMySQL('recipes').query_db(query,data)
        print(results)
        return cls(results[0])

    @classmethod
    def edit(cls,data):
        query = 'update recipes set name = %(name)s, description = %(description)s, date_made = %(date_made)s, instructions =  %(instructions)s, under_30 = %(under_30)s where id = %(id)s;'
        results = connectToMySQL('recipes').query_db(query,data)
        print(results)
        return results

    @classmethod
    def delete(cls,data):
        query = "delete from recipes where id = %(id)s ;"
        return connectToMySQL('recipes').query_db(query,data)

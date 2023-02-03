from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('login_register.html')

@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect('/log_out')
    data ={
        'id': session['user_id']
    }
    user = User.get_by_id(data)
    print(user.first_name)
    recipes = Recipe.get_all_recipes()
    return render_template('welcome_user.html', user = user, recipes = recipes)

@app.route('/log_out')
def log_out():
    session.clear()
    return redirect('/')

@app.route('/creat_user', methods=['POST'])
def creat_user():
    if not User.vlaidate_user(request.form):
        return redirect('/')
    user = User.save(request.form)
    session['user_id'] = user
    return redirect('/recipes')

@app.route('/login', methods =['POST'])
def login():
    user = User.get_email(request.form)
    if not user:
        flash('Invalid email')
        return redirect('/')
    if not  bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid password')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/recipes')

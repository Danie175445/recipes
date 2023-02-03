from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

@app.route('/recipe/new')
def new_recipe():
    return render_template('add_recipe.html')

@app.route('/creat_recipe', methods= ['POST'])
def creat_recipe():
    if not Recipe.validate(request.form):
        return redirect('/recipe/new')
    Recipe.save(request.form)
    return redirect('/recipes')

@app.route('/view_recipe/<int:id>')
def view_recipe(id):
    data ={
        'id': id
    }
    recipe = Recipe.get_recipe(data)
    user = User.get_by_id({'id': session['user_id']})
    return render_template('view_recipe.html', recipe = recipe, user = user)

@app.route('/edit_recipe/<int:id>')
def edit_recipe(id):
    data = {
        'id': id
    }
    recipe = Recipe.get_recipe(data)
    return render_template('edit_recipe.html', recipe = recipe)

@app.route('/update_recipe', methods = ['POST'])
def update_recipe():
    if not Recipe.validate(request.form):
        return redirect(f'/edit_recipe/{request.form["id"]}')
    Recipe.edit(request.form)
    return redirect('/recipes')

@app.route('/delete/<int:id>')
def delete(id):
    data = {
        'id': id
    }
    Recipe.delete(data)
    return redirect('/recipes')
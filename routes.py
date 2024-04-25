from app import app
from flask import render_template, request, redirect
import users
import recipes

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/login", methods=["get", "post"])
def login():
    
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not users.login(username, password):
            return render_template("error.html", message="Väärä tunnus tai salasana")
        return redirect("/")
    
@app.route("/register", methods=["get", "post"])
def register():
    
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="Tunnuksessa tulee olla 1-20 merkkiä")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if password1 == "":
            return render_template("error.html", message="Salasana on tyhjä")
        
        if not users.register(username, password1):
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

        return redirect("/")
    
@app.route("/logout")
def logout():
    
    users.logout()
    return redirect("/")

@app.route("/profile", methods=["get"])
def profile():

    creator_id = users.user_id()

    if request.method == "GET":
        return render_template("profile.html", recipes=recipes.user_recipes(creator_id))

@app.route("/create_recipe", methods=["get", "post"])
def create_recipe():
    
    if request.method == "GET":
        return render_template("create_recipe.html")
    
    if request.method == "POST":
        name = request.form["name"]
        creator_id = users.user_id()
        servings = request.form["servings"]
        categories = request.form.getlist("category")
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]

        if name == "":
            return render_template("error.html", message="Reseptille ei annettu nimeä")

        if ingredients == "":
            return render_template("error.html", message="Ainesosat kenttä on tyhjä") 

        if instructions == "":
            return render_template("error.html", message="Työvaiheet kenttä on tyhjä")
        
        recipe_id = recipes.create_recipe(name, creator_id, servings, categories, ingredients, instructions)
        
        return redirect("/recipe/"+str(recipe_id))
    
@app.route("/recipe/<int:recipe_id>", methods=["get", "post"])
def recipe(recipe_id):

    id = recipe_id
    if request.method == "GET":
        recipe = recipes.recipe(recipe_id)
        name = recipe[0]
        servings = recipe[1]
        ingredients = recipe[2]
        instructions = recipe[3]
        creator_id = recipe[4]

        return render_template("recipe.html", name=name, servings=servings, ingredients=ingredients, instructions=instructions, creator_id=creator_id, id=id)

    if request.method == "POST":
        recipes.remove_recipe(recipe_id)

        return redirect("/profile")
        
    

from app import app
from flask import render_template, request, redirect
import users
import recipes

@app.route("/")
def index():

    return render_template("index.html")

@app.route("/results")
def results():

    search = request.args["search"]

    return render_template("results.html", results=recipes.search_recipes(search))

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

@app.route("/profile", methods=["get", "post"])
def profile():

    if not users.user_id():
        return redirect("/login")
    
    if request.method == "POST":

        if "remove_recipe" in request.form:
            recipe_id = request.form["recipe_id"]
            recipes.remove_recipe(recipe_id)

        return redirect("/profile")
    if request.method == "GET":       
    
        return render_template("profile.html", recipes=recipes.user_recipes(users.user_id()), favourites=recipes.user_favourites(users.user_id()), comments=recipes.user_comments(users.user_id()))

@app.route("/create_recipe", methods=["get", "post"])
def create_recipe():

    if not users.user_id():
        return redirect("/login")
    
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
              
    if request.method == "POST":

        if "comment" in request.form:
            comment = request.form["comment"]
            recipes.add_comment(comment, users.user_id(), recipe_id)
        
        if "add" in request.form:
            recipes.add_favourites(users.user_id(), recipe_id)
        
        if "remove" in request.form:
            recipes.remove_favourites(users.user_id(), recipe_id)

        if "remove_comment" in request.form:
            comment_id = request.form["comment_id"]
            recipes.remove_comment(comment_id)

        return redirect("/recipe/"+str(recipe_id))
    
    if request.method == "GET": 

        in_favourites = False

        for favourite in recipes.user_favourites(users.user_id()):
            if favourite[0] == recipe_id:
                in_favourites = True
                break

        return render_template("recipe.html", recipe=recipes.recipe(recipe_id), user_id=users.user_id(), comments=recipes.recipe_comments(recipe_id), favourites=recipes.user_favourites(users.user_id()), in_favourites=in_favourites)

from db import db
from sqlalchemy.sql import text


def create_recipe(name, creator_id, servings, categories, ingredients, instructions):
    
      sql = text("INSERT INTO recipes (name, creator_id, servings, ingredients, instructions)" \
            " VALUES (:name, :creator_id, :servings, :ingredients, :instructions) RETURNING id")
      
      result = db.session.execute(sql, {"name":name, "creator_id":creator_id, "servings":servings,
                                          "ingredients":ingredients, "instructions":instructions})
      
      recipe_id = result.fetchone()[0]
      
      for category in categories:
            sql = text("SELECT id FROM categories WHERE category=:category")
            result = db.session.execute(sql, {"category":category})
            category_id = result.fetchone()[0]

            sql = text("INSERT INTO recipe_categories (recipe_id, category_id)" \
                       "VALUES (:recipe_id, :category_id)")
            db.session.execute(sql, {"recipe_id":recipe_id, "category_id":category_id})
            db.session.commit()

      return recipe_id

def user_recipes(creator_id):

      sql = text("SELECT id, name FROM recipes WHERE visible=TRUE AND creator_id=:creator_id")

      result = db.session.execute(sql, {"creator_id":creator_id})

      recipes = result.fetchall()

      return recipes

def recipe(recipe_id):

      sql = text("SELECT id, name, servings, ingredients, instructions, creator_id FROM recipes WHERE id=:id")

      result = db.session.execute(sql, {"id":recipe_id})

      recipe = result.fetchone()

      return recipe

def remove_recipe(recipe_id):
      
      sql = text("UPDATE recipes SET visible=FALSE WHERE id=:id")
      db.session.execute(sql, {"id":recipe_id})
      db.session.commit()

def search_recipes(search):

      sql = text("SELECT id, name FROM recipes WHERE visible=:visible AND name ILIKE :search")

      result = db.session.execute(sql, {"visible":True, "search":"%"+search+"%"})

      results = result.fetchall()

      return results

def user_favourites(user_id):

      sql = text("SELECT recipes.id, recipes.name FROM recipes, favourites WHERE favourites.user_id=:user_id AND favourites.recipe_id=recipes.id AND recipes.visible=True")

      result = db.session.execute(sql, {"user_id":user_id})

      favourites = result.fetchall()

      return favourites

def add_favourites(user_id, recipe_id):

        sql = text("INSERT INTO favourites (user_id, recipe_id) VALUES (:user_id, :recipe_id)")
  
        db.session.execute(sql, {"user_id":user_id, "recipe_id":recipe_id})
  
        db.session.commit()
  
def remove_favourites(user_id, recipe_id):
  
        sql = text("DELETE FROM favourites WHERE user_id=:user_id AND recipe_id=:recipe_id")
  
        db.session.execute(sql, {"user_id":user_id, "recipe_id":recipe_id})
  
        db.session.commit()
         
def recipe_comments(recipe_id):

      sql = text("SELECT comments.id, comments.user_id, users.username, comments.comment, comments.recipe_id FROM users, comments WHERE users.id=comments.user_id AND comments.recipe_id=:recipe_id AND visible=True")

      result = db.session.execute(sql, {"recipe_id":recipe_id})

      comments = result.fetchall()

      return comments

def add_comment(comment, user_id, recipe_id):

      sql = text("INSERT INTO comments (comment, user_id, recipe_id) VALUES (:comment, ':user_id', ':recipe_id')")

      db.session.execute(sql, {"comment":comment, "user_id":user_id, "recipe_id":recipe_id})

      db.session.commit()

def remove_comment(comment_id):

      sql = text("UPDATE comments SET visible=False WHERE id=:id")

      db.session.execute(sql, {"id":comment_id})

      db.session.commit()


def user_comments(user_id):

      sql = text("SELECT comments.id, comments.user_id, recipes.id, recipes.name, comments.comment FROM recipes, comments WHERE comments.user_id=:user_id AND comments.recipe_id=recipes.id AND comments.visible=True")

      result = db.session.execute(sql, {"user_id":user_id})

      user_comments = result.fetchall()

      return user_comments




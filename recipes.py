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

      sql = text("SELECT name, servings, ingredients, instructions, creator_id FROM recipes WHERE id=:id")

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




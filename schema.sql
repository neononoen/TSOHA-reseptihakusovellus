CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    creator_id INTEGER REFERENCES users(id),
    servings INTEGER,
    ingredients TEXT,
    instructions TEXT,
    visible BOOLEAN
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    category TEXT
);

CREATE TABLE recipe_categories (
    id SERIAL PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes(id),
    category_id INTEGER REFERENCES categories(id)
);

CREATE TABLE favourites (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    visible BOOLEAN
);

CREATE TABLE  ratings (
    id SERIAL PRIMARY KEY,
    score INTEGER,
    user_id INTEGER REFERENCES users(id),
    recipe_id INTEGER REFERENCES recipes(id)
);

CREATE TABLE  comments (
    id SERIAL PRIMARY KEY,
    comment TEXT,
    user_id INTEGER REFERENCES users(id),
    visible BOOLEAN
);




# Import necessary modules and classes
from flask import flash
from flask_app.models.user import User
from flask_app.config.mysqlconnection import connectToMySQL

# Database name
db_name = "games_library"


# Game class
class Game:
    # Constructor that initializes the attributes of the game object
    def __init__(self, db_data):
        self.id = db_data["id"]
        self.title = db_data["title"]
        self.genre = db_data["genre"]
        self.rating = db_data["rating"]
        self.description = db_data["description"]
        self.release_date = db_data["release_date"]
        self.developer = db_data["developer"]
        self.publisher = db_data["publisher"]
        self.platform = db_data["platform"]
        self.created_at = db_data["created_at"]
        self.updated_at = db_data["updated_at"]
        self.user_id = db_data["user_id"]

    # Class method to get a single game from the database along with the user who posted it
    @classmethod
    def get_one_w_user(cls, data):
        query = """ SELECT * FROM games JOIN users ON users.id = games.user_id WHERE games.id = %(id)s """
        results = connectToMySQL(db_name).query_db(query, data)
        game = cls(results[0])
        posted_by_data = {
            "id": results[0]["users.id"],
            "first_name": results[0]["first_name"],
            "last_name": results[0]["last_name"],
            "email": results[0]["email"],
            "password": results[0]["password"],
            "created_at": results[0]["created_at"],
            "updated_at": results[0]["updated_at"],
        }
        game.user = User(posted_by_data)
        return game

    # Class method to get all games from the database along with the users who are selling them
    @classmethod
    def get_all(cls):
        query = """ SELECT * FROM games JOIN users ON users.id = games.user_id """
        results = connectToMySQL(db_name).query_db(query)
        games = []
        for row in results:
            game = cls(row)
            game_user = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
            }
            game.user = User(game_user)
            games.append(game)
        return games

    # Class method to create a new game in the database
    @classmethod
    def create(cls, form_data):
        query = """ INSERT INTO games (title, genre, rating, description, release_date, developer, publisher, platform,user_id) VALUES (%(title)s, %(genre)s, %(rating)s, %(description)s, %(release_date)s, %(developer)s, %(publisher)s, %(platform)s, %(user_id)s) """
        results = connectToMySQL(db_name).query_db(query, form_data)
        return results

    # Class method to get a single game from the database based on its id
    @classmethod
    def get_one(cls, user_id):
        query = """ SELECT * FROM games WHERE id = %(id)s """
        results = connectToMySQL(db_name).query_db(query, user_id)
        return cls(results[0])

    # Class method to update a game in the database
    @classmethod
    def update(cls, data):
        query = """ UPDATE games SET title = %(title)s, rating = %(rating)s, description = %(description)s, genre = %(genre)s, release_date = %(release_date)s, developer = %(developer)s, publisher = %(publisher)s, platform = %(platform)s,  updated_at = NOW() WHERE id = %(id)s """
        return connectToMySQL(db_name).query_db(query, data)

    # Class method to save a game to the database (either insert a new one or update an existing one)
    @classmethod
    def save(cls, data):
        valid = cls.validate_game(data)
        if not valid:
            return False
        if "id" in data:
            # Update the existing game
            query = """ UPDATE games SET title = %(title)s, genre = %(genre)s, rating = %(rating)s, description = %(description)s, release_date = %(release_date)s, developer = %(developer)s, publisher = %(publisher)s, platform = %(platform)s, updated_at = NOW() WHERE id = %(id)s """
        else:
            # Create a new game
            query = """ INSERT INTO games (title, genre, rating, description, release_date, developer, publisher, platform, user_id) VALUES (%(title)s, %(genre)s, %(rating)s, %(description)s, %(release_date)s, %(developer)s, %(publisher)s, %(platform)s, %(user_id)s) """
        return connectToMySQL(db_name).query_db(query, data)

    # Class method to delete a game from the database
    @classmethod
    def delete(cls, data):
        query = """ DELETE FROM games WHERE id = %(id)s """
        return connectToMySQL(db_name).query_db(query, data)

    # Static method to validate game data before saving or updating
    @staticmethod
    def validate_game(game):
        is_valid = True
        if len(game["title"]) < 3:
            is_valid = False
            flash("Title must be at least 3 characters", "game")
        if len(game["genre"]) < 3:
            is_valid = False
            flash("Genre must be at least 3 characters", "game")
        if len(game["rating"]) < 1:
            is_valid = False
            flash("Rating must be at least 1 character", "game")
        if len(game["description"]) < 3:
            is_valid = False
            flash("Description must be at least 3 characters", "game")
        if len(game["release_date"]) < 1:
            is_valid = False
            flash("Release date must be at least 1 character", "game")
        if len(game["developer"]) < 3:
            is_valid = False
            flash("Developer must be at least 3 characters", "game")
        if len(game["publisher"]) < 3:
            is_valid = False
            flash("Publisher must be at least 3 characters", "game")
        if len(game["platform"]) < 3:
            is_valid = False
            flash("Platform must be at least 3 characters", "game")
        return is_valid

# Import necessary modules and classes
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re

# Create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

# Database name
db_name = "games_library"


# User class
class User:
    # Constructor that initializes the attributes of the User object
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # Class method to get a user by their ID from the database
    @classmethod
    def get_one(cls, data):
        query = """ SELECT * FROM users WHERE id = %(id)s """
        results = connectToMySQL(db_name).query_db(query, data)
        return cls(results[0])

    # Class method to get a user with associated games from the database
    @classmethod
    def get_user_w_games(cls, user_id):
        query = """ SELECT * FROM users
        JOIN games ON games.user_id = users.id = %(id)s """
        results = connectToMySQL(db_name).query_db(query, {"id": user_id})
        user = cls(results[0])
        for row in results:
            game_data = {
                "id": row["games.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"],
            }
            user = User(game_data)
            user.append(game_data)
        return user

    # Class method to get a user by their email from the database
    @classmethod
    def get_by_email(cls, data):
        query = """ SELECT * FROM users WHERE email = %(email)s """
        results = connectToMySQL(db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    # Class method to get a user by their ID from the database
    @classmethod
    def get_by_id(cls, data):
        query = """ SELECT * FROM users WHERE id = %(id)s """
        result = connectToMySQL(db_name).query_db(query, data)
        return cls(result[0]) if result else None

    # Class method to save a user to the database
    @classmethod
    def save(cls, data):
        query = """ INSERT INTO users (first_name, last_name, email, password)
					VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pw_hash)s) """
        return connectToMySQL(db_name).query_db(query, data)

    # Static method to validate user data before saving
    @staticmethod
    def validate_user(user_data):
        # Set is_valid to True
        is_valid = True
        # Test if the first name is at least 2 characters
        if len(user_data["first_name"]) < 3:
            flash("First name must be at least 3 characters", "register")
            is_valid = False
        # Test if the last name is at least 2 characters
        if len(user_data["last_name"]) < 3:
            flash("Last name must be at least 3 characters", "register")
            is_valid = False
        # Test whether email matches the EMAIL_REGEX pattern
        if not EMAIL_REGEX.match(user_data["email"]):
            flash("Email must have a valid email format", "register")
            is_valid = False
        query = """ SELECT * FROM users WHERE email = %(email)s """
        results = connectToMySQL(db_name).query_db(query, user_data)
        # Test if the email is already being used
        if len(results) != 0:
            flash("This email is already being used", "register")
            is_valid = False
        # Test if the password is at least 8 characters
        if len(user_data["password"]) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        # Test if passwords match
        if user_data["password"] != user_data["confirm_password"]:
            flash("Password does not match", "register")
            is_valid = False
        return is_valid

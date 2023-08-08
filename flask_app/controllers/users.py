# Import necessary modules and the Flask app instance
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.game import Game
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


# Route for the home page (registration form)
@app.route("/")
def index():
    return render_template("register.html")


# Route for the main dashboard page
@app.route("/dashboard")
def sec_dashboard():
    # Check if the user is logged in
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id": session["user_id"]}
    all_games = Game.get_all()
    return render_template(
        "dashboard.html", user=User.get_by_id(data), all_games=all_games
    )


# Route for handling user registration form submission
@app.post("/register")
def register():
    if not User.validate_user(request.form):
        return redirect("/")

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"],
    }

    # Hash the password using Bcrypt
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data["pw_hash"] = pw_hash

    # Save the user data to the database
    user = User.save(data)

    if user:
        session["user_id"] = user
        # Redirect to the dashboard after successful registration
        return redirect("/dashboard")
    else:
        # Display flash message for registration failure
        flash("Registration failed, please try again!!!", "register")
        return redirect("/")


# Route for handling user login form submission
@app.post("/login")
def login():
    # Retrieve user data by email
    user_data = User.get_by_email(request.form)

    if not user_data:
        # Display flash message for invalid email
        flash("Invalid Email!!!", "login")
        return redirect("/")

    if not bcrypt.check_password_hash(user_data.password, request.form["password"]):
        # Display flash message for invalid password
        flash("Invalid Password!!!", "login")
        return redirect("/")

    # Set the user_id in the session to indicate the user is logged in
    session["user_id"] = user_data.id
    # Redirect to the dashboard after successful login
    return redirect("/dashboard")


# Route for logging out
@app.route("/logout")
def logout():
    # Clear the session data to log out the user
    session.clear()
    # Redirect to the home page
    return redirect("/")

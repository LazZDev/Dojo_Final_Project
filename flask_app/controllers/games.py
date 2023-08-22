# Import necessary modules and the Flask app instance
from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.game import Game
from flask_app.models.user import User


# Route for displaying the dashboard with all games
@app.route("/dashboard")
def dashboard():
    game = Game.get_all_games()  # Retrieve all games from the database
    # Render the dashboard template with the games data
    return render_template("dashboard.html", all_games=game)


# Route for displaying the form to create a new game
@app.get("/new_game")
def new_game():
    if "user_id" not in session:
        return redirect("/logout")
    # Render the new_game template with user data
    return render_template(
        "new_game.html", user=User.get_by_id({"id": session["user_id"]})
    )


# Route for processing the form to create a new game
@app.post("/create_game")
def create_game():
    if "user_id" not in session:
        return redirect("/logout")
    if not Game.validate_game(request.form):
        # Redirect to the new_game route if form validation fails
        return redirect("/new_game")
    Game.create(request.form)  # Create the new game in the database
    # Redirect to the dashboard after successful creation
    return redirect("/dashboard")


# Route for displaying the form to edit a game
@app.get("/edit_game/<int:id>")
def edit_game(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id": id}
    user_data = {"id": session["user_id"]}
    # Retrieve the game data to be edited from the database
    edit = Game.get_one(data)
    # Render the edit_game template with game and user data
    return render_template("edit_game.html", edit=edit, user=User.get_one(user_data))


# Route for processing the form to update a game
@app.post("/update_game/")
def update_game():
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id": request.form["id"],
        "title": request.form["title"],
        "genre": request.form["genre"],
        "rating": request.form["rating"],
        "description": request.form["description"],
        "release_date": request.form["release_date"],
        "developer": request.form["developer"],
        "publisher": request.form["publisher"],
        "platform": request.form["platform"],
        "user_id": session["user_id"],
    }
    if not Game.validate_game(request.form):
        id = request.form["id"]
        # Redirect to the edit_game route if form validation fails
        return redirect(f"/edit_game/{id}")
    Game.update(data)  # Update the game data in the database
    # Redirect to the dashboard after successful update
    return redirect("/dashboard")


# Route for displaying detailed information about a game
@app.get("/show_game/<int:game_id>")
def show_game(game_id):
    if "user_id" not in session:
        return redirect("/")
    # Retrieve the detailed information about the game from the database
    data = {"id": game_id}
    game = Game.get_one_w_user(data)
    return render_template("show_game.html", game=game)
    # Render the game_info template with game and user data

# Route for deleting a game
@app.get("/delete_game/<int:id>")
def delete_game(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {"id": id}
    Game.delete(data)  # Delete the game from the database
    # Redirect to the dashboard after successful deletion
    return redirect("/dashboard")

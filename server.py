# Import the Flask instance created in the "app.py" file
from flask_app import app

# Import the route handlers for users and cars from the "controllers" package
from flask_app.controllers import users, games

# This block ensures that the application only runs when the script is executed directly, not when imported as a module
if __name__ == "__main__":
    # Run the Flask application with debug mode on, on localhost, and port 5000
    app.run(debug=True, host="localhost", port=5000)
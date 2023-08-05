from flask import Flask

# Create an instance of the Flask class and store it in the variable `app`.
app = Flask(__name__)

# Set the secret key for the Flask app. This key is used for securely signing cookies and sessions.
# It should be a long and random string to enhance security.
app.secret_key = "the final shot!"
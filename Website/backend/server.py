from flask import Flask
from flask_cors import CORS
import sys
import os

# Determine the absolute path to the current file
current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)

# Append the necessary paths based on the current file's location
routes_path = os.path.join(current_directory, "routes")
db_path = os.path.join(current_directory, "db")
utils_path = os.path.join(current_directory, "utils")

sys.path.append(routes_path)
sys.path.append(db_path)
sys.path.append(utils_path)

# connect to the database
from db_connection import db

# Import requests' handlers
from process_request import process_request_bp
from auth import auth_bp
from admin_requests import admin_requests_bp

# Create the Flask app
app = Flask(__name__)
CORS(app, supports_credentials=True)

# Register the blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_requests_bp)
app.register_blueprint(process_request_bp)



if __name__ == "__main__":
    app.run(debug=True)

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

sys.path.append(routes_path)
sys.path.append(db_path)

app = Flask(__name__)
CORS(app)

# Import requests' handlers
from routes.process_request import *
from routes.auth import *


if __name__ == "__main__":
    app.run()

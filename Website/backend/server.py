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

print(routes_path)
print(db_path)

sys.path.append(routes_path)
sys.path.append(db_path)

# Import requests' handlers
from process_request import *
from auth import *
from admin_requests import *



app = Flask(__name__)
CORS(app, supports_credentials=True)


if __name__ == "__main__":
    app.run()

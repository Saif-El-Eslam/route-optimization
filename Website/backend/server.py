from flask import Flask
from flask_cors import CORS
import sys

sys.path.append("f:/FreeLance/yasser/route-optimization/Website/backend/db")
sys.path.append("f:/FreeLance/yasser/route-optimization/Website/backend/routes")

app = Flask(__name__)
CORS(app)

# Import requests' handlers
from routes.process_request import *
from routes.auth import *


if __name__ == "__main__":
    app.run()

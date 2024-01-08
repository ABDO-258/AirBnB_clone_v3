#!/usr/bin/python3
"""hbnb API START"""
from api.v1.views import app_views
from flask import Flask
from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


# Register the blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def errorhandler_404(exc):
    return {
        "error": "Not found"
    }, 404


if __name__ == "__main__":
    """start the app"""
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    # run flask app
    app.run(host=host, port=port, threaded=True)

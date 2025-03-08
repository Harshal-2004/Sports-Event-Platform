import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key_for_development")

# Configure MongoDB
app.config["MONGO_URI"] = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/sports_events")
mongo = PyMongo(app)

# Initialize collections
with app.app_context():
    # These are our main collections
    events_collection = mongo.db.events
    services_collection = mongo.db.services
    packages_collection = mongo.db.packages
    auctions_collection = mongo.db.auctions
    payments_collection = mongo.db.payments
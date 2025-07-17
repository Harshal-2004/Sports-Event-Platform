import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId
from datetime import datetime
from flask_cors import CORS

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Get MongoDB URI

# Get MongoDB URI from environment only
mongo_uri = os.environ.get("MONGODB_URI")
print(f"MONGO_URI: {mongo_uri}")  # Debug print
if not mongo_uri:
    raise ValueError("MONGO_URI is not set! Check your .env file.")

if not mongo_uri:
    raise ValueError("MONGO_URI is not set! Check your .env file.")

# Configure MongoDB
app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)

# Check if connection is established
if mongo.db is None:
    raise ValueError("MongoDB connection failed. Check your URI and network.")

# Define collections
events_collection = mongo.db.events
services_collection = mongo.db.services
packages_collection = mongo.db.packages
auctions_collection = mongo.db.auctions
payments_collection = mongo.db.payments

print("MongoDB Connection Successful!")

# Enable CORS
CORS(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

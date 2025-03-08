
# Sports Event Management Database Setup Guide

## Overview
This document guides you through setting up the database for the Sports Event Management website locally, from installation to configuration and testing.

## Backend Technologies
- **Python Flask**: Web framework
- **SQLAlchemy**: ORM for database interactions
- **PostgreSQL**: Database

## Step 1: Install Required Software
1. Install Python (3.11 or later): https://www.python.org/downloads/
2. Install PostgreSQL: https://www.postgresql.org/download/
3. Install required Python packages:
   ```
   pip install flask flask-sqlalchemy sqlalchemy psycopg2-binary gunicorn email-validator
   ```

## Step 2: Set Up PostgreSQL Database
1. After installing PostgreSQL, open pgAdmin or psql terminal
2. Create a new database named "sports_events":
   ```sql
   CREATE DATABASE sports_events;
   ```
3. Create a new user (optional but recommended):
   ```sql
   CREATE USER sports_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE sports_events TO sports_user;
   ```

## Step 3: Configure Environment Variables
Create a file named `.env` in your project root with the following content:

```
DATABASE_URL=postgresql://sports_user:your_password@localhost:5432/sports_events
SESSION_SECRET=your_session_secret_key
```

## Step 4: Update Database Configuration
Ensure your `app.py` loads environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Import models here
    from models.event import Event
    db.create_all()
```

## Step 5: Database Initialization Script
Create a database initialization script to set up your tables:

```python
# db_init.py
from app import app, db
from models.event import Event

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
```

Run it with:
```
python db_init.py
```

## Step 6: Update main.py for Database Integration
Ensure your `main.py` is updated to use the SQLAlchemy models:

```python
from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import logging
from datetime import datetime
from app import app, db
from models.event import Event

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_pages(path):
    return send_from_directory('.', path)

@app.route('/api/customize', methods=['POST'])
def customize_event():
    try:
        data = request.get_json()
        logger.info(f"Received event customization request: {data}")

        # Create event object
        event = Event(
            sports=data.get('sports', []),
            location=data.get('location'),
            event_date=datetime.fromisoformat(data.get('eventDate').replace('Z', '+00:00')),
            participants=int(data.get('participants', 0)),
            requirements=data.get('requirements')
        )

        # Store event in database
        db.session.add(event)
        db.session.commit()

        logger.info(f"Successfully saved event: {event.to_dict()}")

        return jsonify({
            "status": "success",
            "message": "Event customization request received",
            "data": event.to_dict()
        })

    except Exception as e:
        logger.error(f"Error processing event request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/api/events', methods=['GET'])
def get_events():
    """Endpoint to retrieve all events"""
    events = Event.query.all()
    return jsonify({
        "status": "success",
        "data": [event.to_dict() for event in events]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

## Step 7: Create a .gitignore File
To avoid committing sensitive information, create a `.gitignore` file:

```
.env
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
```

## Step 8: Running the Application Locally
Run your Flask application:

```
python main.py
```

Your application will be accessible at http://localhost:5000

## Step 9: Testing Database Connectivity
1. Navigate to http://localhost:5000/pages/customize.html
2. Fill out and submit the form
3. Check the console logs for success messages
4. Visit http://localhost:5000/api/events to verify your data was saved

## Troubleshooting
- **Database Connection Issues**: Ensure PostgreSQL is running and credentials are correct
- **Missing Modules**: Install any missing Python packages with `pip install`
- **SQLAlchemy Errors**: Check database URL format and table structure
- **Flask Application Errors**: Check console logs for specific error messages

## Next Steps
- Add user authentication
- Implement full CRUD operations for events
- Create an admin dashboard
# Setting Up the MongoDB Database

This guide will help you set up and configure the MongoDB database for the Sports Event Management system.

## Prerequisites

- MongoDB installed locally or a MongoDB Atlas account
- Python 3.x installed

## Step 1: Set Up Environment Variables

Create a `.env` file in the root of your project with the following content:

```
MONGODB_URI=mongodb://localhost:27017/sports_events
SESSION_SECRET=your_secret_key_here
```

If you're using MongoDB Atlas, replace the URI with your connection string:

```
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/sports_events?retryWrites=true&w=majority
```

## Step 2: Run the Database Setup Script

Run the setup script to create the necessary collections and add sample data:

```
python setup_mongo.py
```

The script will:
1. Create all required collections (events, services, packages, auctions, payments)
2. Optionally add sample data for testing

## Step 3: Verify Database Setup

You can verify that the database is set up correctly by running:

```
python view_database.py
```

This will display the collections and their contents.

## Database Schema

The database consists of the following collections:

### Events Collection
- Fields: title, description, date, location, event_type, status, attendees

### Services Collection
- Fields: name, description, price, category

### Packages Collection
- Fields: name, description, price, features (array)

### Auctions Collection
- Fields: title, description, starting_price, current_price, end_date, status, created_at

### Payments Collection
- Fields: amount, payment_date, payment_method, status, item_id, item_type, user_id

## API Endpoints

The application provides the following API endpoints for database interaction:

### Events
- GET /api/events - List all events
- POST /api/events - Create a new event
- GET /api/events/<id> - Get a specific event
- PUT /api/events/<id> - Update an event
- DELETE /api/events/<id> - Delete an event

### Services
- GET /api/services - List all services
- POST /api/services - Add a new service

### Packages
- GET /api/packages - List all packages
- POST /api/packages - Add a new package

### Auctions
- GET /api/auctions - List all auctions
- POST /api/auctions - Create a new auction
- POST /api/auctions/<id>/bid - Place a bid on an auction

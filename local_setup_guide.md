
# Sports Event Management - Local Setup Guide

This guide will help you set up the full Sports Event Management project on your local computer, including MongoDB database and all backend requirements.

## Prerequisites
- Python 3.11 or higher
- MongoDB Community Edition
- Git (optional, for cloning)

## Step 1: Download the Project

### Option 1: Download ZIP
1. Click the three dots (⋮) in the top-right corner of the Replit interface
2. Select "Download as zip"
3. Extract the ZIP file to a folder on your computer

### Option 2: Clone with Git
If you have Git installed, run:
```
git clone https://github.com/your-username/sports-event-management.git
```

## Step 2: Install MongoDB

### Windows
1. Download MongoDB Community Server from [MongoDB website](https://www.mongodb.com/try/download/community)
2. Run the installer and follow the instructions
3. Choose "Complete" installation
4. Install MongoDB Compass (GUI tool) when prompted

### macOS
Using Homebrew:
```
brew tap mongodb/brew
brew install mongodb-community
```

### Linux (Ubuntu/Debian)
```
sudo apt update
sudo apt install -y mongodb
sudo systemctl enable mongodb
sudo systemctl start mongodb
```

## Step 3: Set Up Python Environment

1. Open a terminal/command prompt in your project folder
2. Install required packages:
```
pip install flask flask-pymongo pymongo python-dotenv gunicorn email-validator
```

## Step 4: Configure Environment Variables

1. Create a `.env` file in the project root directory
2. Copy the content from `.env.example` into this file:
```
# MongoDB connection string
MONGODB_URI=mongodb://localhost:27017/sports_events

# Session secret (used for Flask sessions)
SESSION_SECRET=your_random_secret_key_here
```

## Step 5: Initialize the Database

1. Start MongoDB service if not already running:
   - Windows: It should run as a service
   - macOS: `brew services start mongodb-community`
   - Linux: `sudo systemctl start mongodb`

2. Run the database initialization script:
```
python db_init.py
```

You should see messages confirming that sample data has been added to the database.

## Step 6: Run the Application

1. Start the Flask application:
```
python main.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

You should now see the Sports Event Management website running locally.

## Step 7: Testing the API Endpoints

Test the backend API endpoints using tools like Postman, curl, or directly from the browser:

- View all events: http://localhost:5000/api/events
- View all services: http://localhost:5000/api/services
- View all packages: http://localhost:5000/api/packages
- View all auctions: http://localhost:5000/api/auctions

## Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running: `mongo` or `mongosh` should connect to the server
- Check MongoDB service status:
  - Windows: Services app → MongoDB
  - macOS: `brew services list`
  - Linux: `sudo systemctl status mongodb`

### Application Not Starting
- Check for port conflicts on 5000
- Ensure all required packages are installed
- Verify the .env file is in the correct location

### API Endpoints Not Working
- Check MongoDB connection
- Verify collections were initialized properly

## Using MongoDB Compass

MongoDB Compass provides a GUI for managing your MongoDB databases:

1. Open MongoDB Compass
2. Connect to: `mongodb://localhost:27017`
3. You should see the `sports_events` database
4. Browse collections: events, services, packages, auctions

## Project Structure

- `/models`: MongoDB data models
- `/pages`: HTML pages for the frontend
- `/css` & `/js`: Frontend assets
- `app.py`: Flask application setup
- `main.py`: Main application entry point
- `db_init.py`: Database initialization script

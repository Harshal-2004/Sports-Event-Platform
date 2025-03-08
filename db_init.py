
# Database initialization script
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from app import app, db
from models.event import Event

with app.app_context():
    # Create all tables in the database
    db.create_all()
    print("Database tables created successfully!")
    
    # You can add sample data here if needed
    # sample_event = Event(
    #     sports=["football", "basketball"],
    #     location="Mumbai",
    #     event_date=datetime.now(),
    #     participants=100,
    #     requirements="Sample event for testing"
    # )
    # db.session.add(sample_event)
    # db.session.commit()
    # print("Sample data added successfully!")

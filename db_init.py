
# Database initialization script for MongoDB
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

from app import app, mongo, events_collection, services_collection, packages_collection, auctions_collection
from models.event import Event
from models.service import Service
from models.package import Package
from models.auction import Auction

def init_database():
    """Initialize the MongoDB database with collections and sample data"""
    with app.app_context():
        # Clear existing data (optional)
        events_collection.delete_many({})
        services_collection.delete_many({})
        packages_collection.delete_many({})
        auctions_collection.delete_many({})
        
        print("Existing collections cleared.")
        
        # Add sample services
        services = [
            Service(
                name="Venue Booking",
                description="Premium sports venues with all facilities",
                price=500.00,
                category="Venue"
            ),
            Service(
                name="Equipment Rental",
                description="Professional sports equipment for all participants",
                price=200.00,
                category="Equipment"
            ),
            Service(
                name="Professional Referee",
                description="Certified referees for official games",
                price=150.00,
                category="Officials"
            ),
            Service(
                name="Medical Staff",
                description="On-site medical professionals for emergencies",
                price=300.00,
                category="Safety"
            ),
            Service(
                name="Event Photography",
                description="Professional photography coverage of your event",
                price=250.00,
                category="Media"
            ),
            Service(
                name="Live Streaming",
                description="Live broadcast of your event online",
                price=400.00,
                category="Media"
            )
        ]
        
        for service in services:
            service.save(services_collection)
            
        print(f"Added {len(services)} sample services.")
        
        # Add sample packages
        packages = [
            Package(
                name="Platinum",
                description="All-inclusive premium sports event management package",
                price=5000.00,
                features=[
                    "Premium venue booking",
                    "Professional equipment",
                    "Certified referees",
                    "Medical staff",
                    "Event photography",
                    "Live streaming",
                    "VIP catering",
                    "Personalized jerseys",
                    "Award ceremony"
                ]
            ),
            Package(
                name="Gold",
                description="Comprehensive sports event management package",
                price=3000.00,
                features=[
                    "Standard venue booking",
                    "Quality equipment",
                    "Certified referees",
                    "Basic medical support",
                    "Event photography",
                    "Basic refreshments"
                ]
            )
        ]
        
        for package in packages:
            package.save(packages_collection)
            
        print(f"Added {len(packages)} sample packages.")
        
        # Add sample auction (optional)
        auction = Auction(
            title="Celebrity Sports Coach Session",
            description="Exclusive training session with a celebrity sports coach",
            starting_price=1000.00,
            current_price=1000.00,
            end_date=datetime.utcnow() + timedelta(days=7)
        )
        auction.save(auctions_collection)
        
        print("Added sample auction.")
        
        print("Database initialization complete!")

if __name__ == "__main__":
    init_database()

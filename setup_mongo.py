
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
import sys

# Load environment variables
load_dotenv()

# MongoDB connection string
MONGO_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/sports_events')

def create_collections():
    """Create all necessary collections for the application"""
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client.get_default_database()
        
        # Create collections if they don't exist
        if 'events' not in db.list_collection_names():
            db.create_collection('events')
            print("✅ Created 'events' collection")
        else:
            print("ℹ️ 'events' collection already exists")
            
        if 'services' not in db.list_collection_names():
            db.create_collection('services')
            print("✅ Created 'services' collection")
        else:
            print("ℹ️ 'services' collection already exists")
            
        if 'packages' not in db.list_collection_names():
            db.create_collection('packages')
            print("✅ Created 'packages' collection")
        else:
            print("ℹ️ 'packages' collection already exists")
            
        if 'auctions' not in db.list_collection_names():
            db.create_collection('auctions')
            print("✅ Created 'auctions' collection")
        else:
            print("ℹ️ 'auctions' collection already exists")
            
        if 'payments' not in db.list_collection_names():
            db.create_collection('payments')
            print("✅ Created 'payments' collection")
        else:
            print("ℹ️ 'payments' collection already exists")
            
        print("\n✅ Database setup complete!")
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        return False

def add_sample_data():
    """Add sample data to the collections for testing"""
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI)
        db = client.get_default_database()
        
        # Add sample services
        services = [
            {
                "name": "Venue Booking",
                "description": "Premium sports venues with all facilities",
                "price": 500.00,
                "category": "Venue"
            },
            {
                "name": "Equipment Rental",
                "description": "Professional sports equipment for all participants",
                "price": 200.00,
                "category": "Equipment"
            },
            {
                "name": "Professional Referee",
                "description": "Certified referees for official games",
                "price": 150.00,
                "category": "Officials"
            }
        ]
        
        if db.services.count_documents({}) == 0:
            db.services.insert_many(services)
            print(f"✅ Added {len(services)} sample services")
        else:
            print("ℹ️ Services collection already has data")
        
        # Add sample packages
        packages = [
            {
                "name": "Platinum",
                "description": "All-inclusive premium sports event management package",
                "price": 5000.00,
                "features": [
                    "Premium venue booking",
                    "Professional equipment",
                    "Certified referees",
                    "Medical staff",
                    "Event photography",
                    "Live streaming"
                ]
            },
            {
                "name": "Gold",
                "description": "Comprehensive sports event management package",
                "price": 3000.00,
                "features": [
                    "Standard venue booking",
                    "Quality equipment",
                    "Certified referees",
                    "Basic medical support"
                ]
            }
        ]
        
        if db.packages.count_documents({}) == 0:
            db.packages.insert_many(packages)
            print(f"✅ Added {len(packages)} sample packages")
        else:
            print("ℹ️ Packages collection already has data")
        
        # Add sample auction
        auction = {
            "title": "Celebrity Sports Coach Session",
            "description": "Exclusive training session with a celebrity sports coach",
            "starting_price": 1000.00,
            "current_price": 1000.00,
            "end_date": datetime.utcnow() + timedelta(days=7),
            "status": "active",
            "created_at": datetime.utcnow()
        }
        
        if db.auctions.count_documents({}) == 0:
            db.auctions.insert_one(auction)
            print("✅ Added sample auction")
        else:
            print("ℹ️ Auctions collection already has data")
        
        print("\n✅ Sample data added successfully!")
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error adding sample data: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Sports Event Management Database Setup ===\n")
    
    if create_collections():
        choice = input("\nDo you want to add sample data to the database? (y/n): ")
        if choice.lower() == 'y':
            add_sample_data()
        
    print("\nSetup complete!")

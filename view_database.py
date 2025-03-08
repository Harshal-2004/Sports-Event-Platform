
from app import app, mongo, events_collection, services_collection, packages_collection, auctions_collection
from bson import json_util
import json

def format_collection(collection, name):
    """Format a collection's data for display"""
    print(f"\n--- {name.upper()} COLLECTION ---")
    items = list(collection.find())
    if not items:
        print("No data found")
        return
    
    for item in items:
        # Convert ObjectId to string for better display
        if '_id' in item:
            item['_id'] = str(item['_id'])
        
        # Handle datetime objects for better display
        print(json.dumps(json.loads(json_util.dumps(item)), indent=2))
        print("-------------------")

def view_database():
    """View the contents of the database collections"""
    with app.app_context():
        # Check each collection
        format_collection(events_collection, "Events")
        format_collection(services_collection, "Services")
        format_collection(packages_collection, "Packages")
        format_collection(auctions_collection, "Auctions")
        
        # Get database stats
        db = mongo.db
        print("\n--- DATABASE STATISTICS ---")
        collections = db.list_collection_names()
        print(f"Collections: {collections}")
        
        total_docs = 0
        for collection_name in collections:
            count = db[collection_name].count_documents({})
            total_docs += count
            print(f"{collection_name}: {count} documents")
        
        print(f"Total documents: {total_docs}")

if __name__ == "__main__":
    view_database()

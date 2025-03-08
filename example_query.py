
from app import app, mongo, events_collection
from datetime import datetime

def example_query():
    with app.app_context():
        # Example: Find all events in a specific location
        events = list(events_collection.find({"location": "mumbai"}))
        print(f"Found {len(events)} events in Mumbai")
        
        # Example: Count services by category
        pipeline = [
            {"$group": {"_id": "$category", "count": {"$sum": 1}}}
        ]
        categories = list(mongo.db.services.aggregate(pipeline))
        print("\nServices by category:")
        for category in categories:
            print(f"{category['_id']}: {category['count']} services")

if __name__ == "__main__":
    example_query()

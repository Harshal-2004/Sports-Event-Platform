
from app import app, events_collection
from bson import json_util
import json

def view_events():
    """View only the contents of the events collection"""
    with app.app_context():
        print("\n--- EVENTS COLLECTION ---")
        events = list(events_collection.find())
        if not events:
            print("No events found")
            return
        
        for event in events:
            # Convert ObjectId to string for better display
            if '_id' in event:
                event['_id'] = str(event['_id'])
            
            # Handle datetime objects for better display
            print(json.dumps(json.loads(json_util.dumps(event)), indent=2))
            print("-------------------")

if __name__ == "__main__":
    view_events()

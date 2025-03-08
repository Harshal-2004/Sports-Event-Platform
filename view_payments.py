
from app import app, payments_collection
from bson import json_util
import json

def view_payments():
    """View only the contents of the payments collection"""
    with app.app_context():
        print("\n--- PAYMENTS COLLECTION ---")
        payments = list(payments_collection.find())
        if not payments:
            print("No payments found")
            return
        
        for payment in payments:
            # Convert ObjectId to string for better display
            if '_id' in payment:
                payment['_id'] = str(payment['_id'])
            
            # Handle datetime objects for better display
            print(json.dumps(json.loads(json_util.dumps(payment)), indent=2))
            print("-------------------")

if __name__ == "__main__":
    view_payments()


from app import app, mongo
import pymongo

def check_collections():
    """Check what collections exist in the database"""
    with app.app_context():
        db = mongo.db
        collections = db.list_collection_names()
        
        print("\n=== DATABASE COLLECTIONS ===")
        print(f"Collections found: {collections}")
        
        # Check if we have the expected collections
        expected = ['events', 'services', 'packages', 'auctions', 'payments']
        missing = [coll for coll in expected if coll not in collections]
        
        if missing:
            print(f"\nMissing collections: {missing}")
            print("These will be created automatically when data is first added to them.")
        else:
            print("\nAll expected collections exist!")
            
        # Show counts for existing collections
        print("\n=== DOCUMENT COUNTS ===")
        for coll in collections:
            count = db[coll].count_documents({})
            print(f"{coll}: {count} documents")

if __name__ == "__main__":
    check_collections()

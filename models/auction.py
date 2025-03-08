
from datetime import datetime
from bson import ObjectId

class Auction:
    def __init__(self, title, description, starting_price, current_price, end_date, status="active", created_at=None, _id=None):
        self.title = title
        self.description = description
        self.starting_price = starting_price
        self.current_price = current_price
        self.end_date = end_date
        self.status = status
        self.created_at = created_at if created_at else datetime.utcnow()
        self._id = _id

    @classmethod
    def from_dict(cls, data):
        """Create an Auction object from a dictionary"""
        if '_id' in data:
            data['_id'] = str(data['_id']) if isinstance(data['_id'], ObjectId) else data['_id']
        return cls(**data)

    def to_dict(self):
        """Convert Auction object to a dictionary"""
        result = {
            'title': self.title,
            'description': self.description,
            'starting_price': self.starting_price,
            'current_price': self.current_price,
            'end_date': self.end_date.isoformat() if isinstance(self.end_date, datetime) else self.end_date,
            'status': self.status,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
        if hasattr(self, '_id') and self._id:
            result['id'] = str(self._id)
        return result

    def save(self, collection):
        """Save auction to MongoDB collection"""
        auction_dict = {
            'title': self.title,
            'description': self.description,
            'starting_price': self.starting_price,
            'current_price': self.current_price,
            'end_date': self.end_date,
            'status': self.status,
            'created_at': self.created_at
        }
        
        if hasattr(self, '_id') and self._id:
            collection.update_one({'_id': ObjectId(self._id)}, {'$set': auction_dict})
        else:
            result = collection.insert_one(auction_dict)
            self._id = result.inserted_id
            
        return self

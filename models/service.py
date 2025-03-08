
from datetime import datetime
from bson import ObjectId

class Service:
    def __init__(self, name, description, price, category=None, _id=None):
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        self.created_at = datetime.utcnow()
        self._id = _id

    @classmethod
    def from_dict(cls, data):
        """Create a Service object from a dictionary"""
        if '_id' in data:
            data['_id'] = str(data['_id']) if isinstance(data['_id'], ObjectId) else data['_id']
        return cls(**data)

    def to_dict(self):
        """Convert Service object to a dictionary"""
        result = {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
        if hasattr(self, '_id') and self._id:
            result['id'] = str(self._id)
        return result

    def save(self, collection):
        """Save service to MongoDB collection"""
        service_dict = {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'created_at': self.created_at
        }
        
        if hasattr(self, '_id') and self._id:
            collection.update_one({'_id': ObjectId(self._id)}, {'$set': service_dict})
        else:
            result = collection.insert_one(service_dict)
            self._id = result.inserted_id
            
        return self

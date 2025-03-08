
from datetime import datetime
from bson import ObjectId

class Package:
    def __init__(self, name, description, price, features=None, _id=None):
        self.name = name
        self.description = description
        self.price = price
        self.features = features or []
        self.created_at = datetime.utcnow()
        self._id = _id

    @classmethod
    def from_dict(cls, data):
        """Create a Package object from a dictionary"""
        if '_id' in data:
            data['_id'] = str(data['_id']) if isinstance(data['_id'], ObjectId) else data['_id']
        return cls(**data)

    def to_dict(self):
        """Convert Package object to a dictionary"""
        result = {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'features': self.features,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
        if hasattr(self, '_id') and self._id:
            result['id'] = str(self._id)
        return result

    def save(self, collection):
        """Save package to MongoDB collection"""
        package_dict = {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'features': self.features,
            'created_at': self.created_at
        }
        
        if hasattr(self, '_id') and self._id:
            collection.update_one({'_id': ObjectId(self._id)}, {'$set': package_dict})
        else:
            result = collection.insert_one(package_dict)
            self._id = result.inserted_id
            
        return self

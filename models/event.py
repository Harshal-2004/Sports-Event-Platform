
from datetime import datetime
from bson import ObjectId

class Event:
    def __init__(self, sports, location, event_date, participants, requirements=None, _id=None):
        self.sports = sports
        self.location = location
        self.event_date = event_date
        self.participants = participants
        self.requirements = requirements
        self.created_at = datetime.utcnow()
        self._id = _id

    @classmethod
    def from_dict(cls, data):
        """Create an Event object from a dictionary"""
        if '_id' in data:
            data['_id'] = str(data['_id']) if isinstance(data['_id'], ObjectId) else data['_id']
        return cls(**data)

    def to_dict(self):
        """Convert Event object to a dictionary"""
        result = {
            'sports': self.sports,
            'location': self.location,
            'event_date': self.event_date.isoformat() if isinstance(self.event_date, datetime) else self.event_date,
            'participants': self.participants,
            'requirements': self.requirements,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
        if hasattr(self, '_id') and self._id:
            result['id'] = str(self._id)
        return result

    def save(self, collection):
        """Save event to MongoDB collection"""
        event_dict = {
            'sports': self.sports,
            'location': self.location,
            'event_date': self.event_date,
            'participants': self.participants,
            'requirements': self.requirements,
            'created_at': self.created_at
        }
        
        if hasattr(self, '_id') and self._id:
            collection.update_one({'_id': ObjectId(self._id)}, {'$set': event_dict})
        else:
            result = collection.insert_one(event_dict)
            self._id = result.inserted_id
            
        return self

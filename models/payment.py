
from datetime import datetime
from bson import ObjectId

class Payment:
    def __init__(self, amount, payment_method, status, event_id=None, service_ids=None, 
                 package_id=None, auction_id=None, user_info=None, _id=None):
        self.amount = amount
        self.payment_method = payment_method
        self.status = status
        self.event_id = event_id
        self.service_ids = service_ids or []
        self.package_id = package_id
        self.auction_id = auction_id
        self.user_info = user_info or {}
        self.created_at = datetime.utcnow()
        self._id = _id

    @classmethod
    def from_dict(cls, data):
        """Create a Payment object from a dictionary"""
        if '_id' in data:
            data['_id'] = str(data['_id']) if isinstance(data['_id'], ObjectId) else data['_id']
        return cls(**data)

    def to_dict(self):
        """Convert Payment object to a dictionary"""
        result = {
            'amount': self.amount,
            'payment_method': self.payment_method,
            'status': self.status,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
        
        if self.event_id:
            result['event_id'] = str(self.event_id)
        if self.service_ids:
            result['service_ids'] = [str(id) for id in self.service_ids]
        if self.package_id:
            result['package_id'] = str(self.package_id)
        if self.auction_id:
            result['auction_id'] = str(self.auction_id)
        if self.user_info:
            result['user_info'] = self.user_info
        if hasattr(self, '_id') and self._id:
            result['id'] = str(self._id)
            
        return result

    def save(self, collection):
        """Save payment to MongoDB collection"""
        payment_dict = {
            'amount': self.amount,
            'payment_method': self.payment_method,
            'status': self.status,
            'created_at': self.created_at
        }
        
        if self.event_id:
            payment_dict['event_id'] = ObjectId(self.event_id) if isinstance(self.event_id, str) else self.event_id
        if self.service_ids:
            payment_dict['service_ids'] = [ObjectId(id) if isinstance(id, str) else id for id in self.service_ids]
        if self.package_id:
            payment_dict['package_id'] = ObjectId(self.package_id) if isinstance(self.package_id, str) else self.package_id
        if self.auction_id:
            payment_dict['auction_id'] = ObjectId(self.auction_id) if isinstance(self.auction_id, str) else self.auction_id
        if self.user_info:
            payment_dict['user_info'] = self.user_info
        
        if hasattr(self, '_id') and self._id:
            collection.update_one({'_id': ObjectId(self._id)}, {'$set': payment_dict})
        else:
            result = collection.insert_one(payment_dict)
            self._id = result.inserted_id
            
        return self

from datetime import datetime
from app import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sports = db.Column(db.JSON, nullable=False)  # Store list of selected sports
    location = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    participants = db.Column(db.Integer, nullable=False)
    requirements = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'sports': self.sports,
            'location': self.location,
            'event_date': self.event_date.isoformat(),
            'participants': self.participants,
            'requirements': self.requirements,
            'created_at': self.created_at.isoformat()
        }

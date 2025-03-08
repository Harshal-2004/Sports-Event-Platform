from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import logging
from datetime import datetime
from app import app, db
from models.event import Event

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_pages(path):
    return send_from_directory('.', path)

@app.route('/api/customize', methods=['POST'])
def customize_event():
    try:
        data = request.get_json()
        logger.info(f"Received event customization request: {data}")

        # Parse date from string to datetime
        event_date = None
        if data.get('eventDate'):
            try:
                event_date = datetime.fromisoformat(data.get('eventDate').replace('Z', '+00:00'))
            except ValueError:
                event_date = datetime.strptime(data.get('eventDate'), '%Y-%m-%d')

        # Create event object
        event = Event(
            sports=data.get('sports', []),
            location=data.get('location'),
            event_date=event_date,
            participants=int(data.get('participants', 0)),
            requirements=data.get('requirements')
        )

        # Store event in database
        db.session.add(event)
        db.session.commit()

        logger.info(f"Successfully saved event: {event.to_dict()}")

        return jsonify({
            "status": "success",
            "message": "Event customization request received",
            "data": event.to_dict()
        })

    except Exception as e:
        logger.error(f"Error processing event request: {str(e)}")
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/api/events', methods=['GET'])
def get_events():
    """Endpoint to retrieve all events"""
    all_events = Event.query.all()
    return jsonify({
        "status": "success",
        "data": [event.to_dict() for event in all_events]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
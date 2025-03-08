from flask import Flask, render_template, send_from_directory, request, jsonify
from datetime import datetime
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from app import app, db
from models.event import Event

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

        # Convert date string to datetime
        date_str = data.get('eventDate')
        if len(date_str) <= 2:  # If it's just a month number
            current_year = datetime.now().year
            event_date = datetime(current_year, int(date_str), 1)
        else:
            event_date = datetime.strptime(date_str, '%Y-%m-%d')

        # Create new event
        new_event = Event(
            sports=data.get('sports'),
            location=data.get('location'),
            event_date=event_date,
            participants=int(data.get('participants')),
            requirements=data.get('requirements')
        )

        # Save to database
        db.session.add(new_event)
        db.session.commit()

        logger.info(f"Successfully saved event: {new_event.to_dict()}")

        return jsonify({
            "status": "success",
            "message": "Event customization request received",
            "data": new_event.to_dict()
        })

    except Exception as e:
        logger.error(f"Error processing event request: {str(e)}")
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
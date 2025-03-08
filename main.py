from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path='', static_folder='.', template_folder='.')

# In-memory storage for now (will be replaced with database later)
events = []

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

        # Create event dictionary
        event = {
            'id': len(events) + 1,
            'sports': data.get('sports', []),
            'location': data.get('location'),
            'event_date': data.get('eventDate'),
            'participants': int(data.get('participants', 0)),
            'requirements': data.get('requirements'),
            'created_at': datetime.now().isoformat()
        }

        # Store event in memory
        events.append(event)

        logger.info(f"Successfully saved event: {event}")

        return jsonify({
            "status": "success",
            "message": "Event customization request received",
            "data": event
        })

    except Exception as e:
        logger.error(f"Error processing event request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

@app.route('/api/events', methods=['GET'])
def get_events():
    """Endpoint to retrieve all events (for testing purposes)"""
    return jsonify({
        "status": "success",
        "data": events
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
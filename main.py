from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_url_path='', static_folder='.', template_folder='.')

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

        # For now, just log and return the data
        # Database integration will be added later
        return jsonify({
            "status": "success",
            "message": "Event customization request received",
            "data": data
        })

    except Exception as e:
        logger.error(f"Error processing event request: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
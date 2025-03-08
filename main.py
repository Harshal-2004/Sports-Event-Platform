from flask import Flask, render_template, send_from_directory, request, jsonify
import os

app = Flask(__name__, 
            static_url_path='',
            static_folder='.',
            template_folder='.')

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_pages(path):
    return send_from_directory('.', path)

@app.route('/api/customize', methods=['POST'])
def customize_event():
    data = request.get_json()
    # TODO: Implement database storage
    return jsonify({
        "status": "success",
        "message": "Event customization request received",
        "data": data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
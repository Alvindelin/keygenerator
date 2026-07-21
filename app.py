from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from check import check_bp
from validate import create_key, load_keys
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# Register blueprint
app.register_blueprint(check_bp)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    key, expiry = create_key()
    return jsonify({
        "success": True,
        "key": key,
        "expiry": expiry,
        "duration": "24h"
    })

@app.route('/api/keys', methods=['GET'])
def list_keys():
    keys = load_keys()
    return jsonify({
        "total": len(keys),
        "keys": keys
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

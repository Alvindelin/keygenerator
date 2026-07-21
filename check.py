from flask import Blueprint, request, jsonify
from validate import validate_key, get_key_status

check_bp = Blueprint('check', __name__)

@check_bp.route('/api/check', methods=['POST'])
def check():
    data = request.get_json() or {}
    key = data.get('key', '').upper()
    device_id = data.get('device_id', '')
    
    is_valid, response = validate_key(key, device_id)
    
    if is_valid:
        return jsonify(response), 200
    else:
        return jsonify({
            "valid": False,
            "message": response.get('message', 'Invalid'),
            "error": response.get('error', 'Unknown'),
            "code": response.get('code', 400)
        }), response.get('code', 400)

@check_bp.route('/api/status/<key>', methods=['GET'])
def status(key):
    key = key.upper()
    key_data = get_key_status(key)
    
    if not key_data:
        return jsonify({
            "exists": False,
            "message": "Key not found"
        }), 404
    
    from datetime import datetime
    expiry = datetime.fromisoformat(key_data['expiry'])
    is_expired = datetime.now() > expiry
    
    return jsonify({
        "exists": True,
        "key": key,
        "created_at": key_data['created_at'],
        "expiry": key_data['expiry'],
        "is_expired": is_expired,
        "used": key_data['used'],
        "device_id": key_data.get('device_id')
    })

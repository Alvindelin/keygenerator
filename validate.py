import json
import os
from datetime import datetime

KEYS_FILE = "keys.json"

def load_keys():
    if not os.path.exists(KEYS_FILE):
        return {}
    with open(KEYS_FILE, 'r') as f:
        return json.load(f)

def save_keys(keys):
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=2)

def generate_key():
    import secrets
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    key = ''.join(secrets.choice(chars) for _ in range(15))
    return f"{key[:5]}-{key[5:10]}-{key[10:15]}"

def create_key():
    keys = load_keys()
    key = generate_key()
    
    # Cek duplikat
    while key in keys:
        key = generate_key()
    
    expiry = (datetime.now() + timedelta(hours=24)).isoformat()
    
    keys[key] = {
        "created_at": datetime.now().isoformat(),
        "expiry": expiry,
        "duration": "24h",
        "used": False,
        "device_id": None,
        "activated_at": None
    }
    save_keys(keys)
    return key, expiry

def validate_key(key, device_id):
    keys = load_keys()
    
    if not key:
        return False, {"message": "Key tidak boleh kosong!", "code": 400}
    
    if key not in keys:
        return False, {"message": "Key tidak ditemukan!", "error": "Key Not Found", "code": 404}
    
    key_data = keys[key]
    expiry = datetime.fromisoformat(key_data['expiry'])
    
    if datetime.now() > expiry:
        return False, {"message": "Key sudah expired!", "error": "Key Expired", "code": 403}
    
    if key_data['used'] and key_data['device_id'] != device_id:
        return False, {"message": "Key sudah dipakai di device lain!", "error": "Forbidden", "code": 403}
    
    # Mark as used
    if not key_data['used']:
        keys[key]['used'] = True
        keys[key]['device_id'] = device_id
        keys[key]['activated_at'] = datetime.now().isoformat()
        save_keys(keys)
    
    return True, {
        "valid": True,
        "status": "Active",
        "expiry": key_data['expiry'],
        "duration": key_data['duration']
    }

def get_key_status(key):
    keys = load_keys()
    if key not in keys:
        return None
    return keys[key]

# Fix import
from datetime import timedelta

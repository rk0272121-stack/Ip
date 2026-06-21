from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import socket
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Sabhi domains ko allow karo

def get_ip_info(ip):
    result = {
        "ip": ip,
        "timestamp": datetime.now().isoformat(),
        "location": {}
    }
    
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
        r = requests.get(url, timeout=3)
        data = r.json()
        if data.get('status') == 'success':
            result['location'] = {
                'ip': data.get('query'),
                'country': data.get('country'),
                'country_code': data.get('countryCode'),
                'region': data.get('regionName'),
                'city': data.get('city'),
                'zip': data.get('zip'),
                'latitude': data.get('lat'),
                'longitude': data.get('lon'),
                'timezone': data.get('timezone'),
                'isp': data.get('isp'),
                'organization': data.get('org'),
                'as': data.get('as'),
            }
    except:
        pass
    
    return result

@app.route('/')
def home():
    return jsonify({
        "name": "NEUTRONNNN_KILLER IP API",
        "status": "🔥 LIVE",
        "endpoints": {
            "/ip": "Your IP",
            "/ip/{ip}": "IP Location Info",
            "/health": "Health Check"
        }
    })

@app.route('/ip')
def get_my_ip():
    ip = request.remote_addr
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return jsonify({"ip": ip, "message": "Your IP address"})

@app.route('/ip/<ip>')
def get_ip(ip):
    if not re.match(r'^\d+\.\d+\.\d+\.\d+$', ip):
        try:
            ip = socket.gethostbyname(ip)
        except:
            return jsonify({"error": "Invalid IP or domain"}), 400
    
    data = get_ip_info(ip)
    return jsonify(data)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

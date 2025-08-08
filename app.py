from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Mengizinkan CORS untuk komunikasi dengan frontend

# Simpan lokasi terakhir
last_location = {"latitude": None, "longitude": None}

# Simpan data signaling
signals = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/child')
def child():
    return render_template('child.html')

@app.route('/parent')
def parent():
    return render_template('parent.html')

@app.route('/update_location', methods=['POST'])
def update_location():
    global last_location
    try:
        data = request.get_json()
        if not data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({"error": "Latitude dan longitude diperlukan"}), 400
        print('Received location:', data)  # Logging untuk debugging
        last_location = {
            "latitude": data['latitude'],
            "longitude": data['longitude']
        }
        return jsonify({"status": "success", "message": "Lokasi diterima"})
    except Exception as e:
        print('Error updating location:', str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/get_location', methods=['GET'])
def get_location():
    return jsonify(last_location)

@app.route('/generate_code', methods=['GET'])
def generate_code():
    try:
        code = str(random.randint(100000, 999999))
        return jsonify({"code": code})
    except Exception as e:
        print('Error generating code:', str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/store_signal', methods=['POST'])
def store_signal():
    try:
        data = request.get_json()
        if not data or 'code' not in data or 'signal' not in data:
            return jsonify({"error": "Code dan signal diperlukan"}), 400
        signals[data['code']] = data['signal']
        print('Stored signal for code:', data['code'])
        return jsonify({"status": "success", "message": "Signal disimpan"})
    except Exception as e:
        print('Error storing signal:', str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/get_signal', methods=['GET'])
def get_signal():
    try:
        code = request.args.get('code')
        if not code:
            return jsonify({"error": "Code diperlukan"}), 400
        signal = signals.get(code, None)
        return jsonify({"signal": signal})
    except Exception as e:
        print('Error getting signal:', str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
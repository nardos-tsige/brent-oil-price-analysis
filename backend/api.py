from flask import Flask, jsonify, request
from flask_cors import CORS
from data_loader import DataLoader
import os

app = Flask(__name__)
CORS(app)

# Initialize data loader
data_loader = DataLoader()

@app.route('/', methods=['GET'])
def home():
    return jsonify({'status': 'healthy', 'message': 'Brent Oil API is running'})

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'API is running'})

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """Get price data with optional date filters"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        data = data_loader.get_price_data(start_date, end_date)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get events with optional category filter"""
    try:
        category = request.args.get('category')
        data = data_loader.get_events(category)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all event categories"""
    try:
        data = data_loader.get_categories()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get basic statistics"""
    try:
        data = data_loader.get_statistics()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/impacts', methods=['GET'])
def get_impacts():
    """Get event impacts"""
    try:
        window = int(request.args.get('window', 10))
        data = data_loader.get_event_impacts(window)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/change-point', methods=['GET'])
def get_change_point():
    """Get detected change point"""
    try:
        data = data_loader.detect_change_point()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
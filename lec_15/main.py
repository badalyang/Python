from flask import Flask, request, jsonify
import json
import os

def atomic_write(filepath, data):
    """Write JSON data to a file atomically."""
    temp_path = filepath + '.tmp'
    with open(temp_path, 'w') as temp_file:
        json.dump(data, temp_file, indent=4, sort_keys=True)
    os.replace(temp_path, filepath)

app = Flask(__name__)

DATA_FILE = 'cars.json'

def load_data():
    """Load car data from a JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(data):
    """Save car data to a JSON file."""
    atomic_write(DATA_FILE, data)

@app.route('/cars', methods=['GET'])
def get_cars():
    """Retrieve all cars."""
    cars = load_data()
    return jsonify({"status": "success", "data": cars}), 200

@app.route('/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    """Retrieve a specific car by ID."""
    cars = load_data()
    car = next((c for c in cars if c['id'] == car_id), None)
    if car is None:
        return jsonify({'status': 'error', 'message': 'Car not found'}), 404
    return jsonify({"status": "success", "data": car}), 200

@app.route('/cars', methods=['POST'])
def create_car():
    """Create a new car."""
    cars = load_data()
    new_car = request.json

    if not all(k in new_car for k in ('make', 'model', 'year', 'price')):
        return jsonify({'status': 'error', 'message': 'Missing car attributes'}), 400

    if not isinstance(new_car['year'], int) or new_car['year'] <= 0:
        return jsonify({'status': 'error', 'message': 'Invalid year value'}), 400

    if not isinstance(new_car['price'], (int, float)) or new_car['price'] < 0:
        return jsonify({'status': 'error', 'message': 'Invalid price value'}), 400

    new_car['id'] = max((c['id'] for c in cars), default=0) + 1
    cars.append(new_car)
    save_data(cars)
    return jsonify({"status": "success", "data": new_car}), 201

@app.route('/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    """Update an existing car by ID."""
    cars = load_data()
    car = next((c for c in cars if c['id'] == car_id), None)
    if car is None:
        return jsonify({'status': 'error', 'message': 'Car not found'}), 404

    updated_data = request.json
    if 'year' in updated_data and (not isinstance(updated_data['year'], int) or updated_data['year'] <= 0):
        return jsonify({'status': 'error', 'message': 'Invalid year value'}), 400

    if 'price' in updated_data and (not isinstance(updated_data['price'], (int, float)) or updated_data['price'] < 0):
        return jsonify({'status': 'error', 'message': 'Invalid price value'}), 400

    for key in ('make', 'model', 'year', 'price'):
        if key in updated_data:
            car[key] = updated_data[key]

    save_data(cars)
    return jsonify({"status": "success", "data": car}), 200

@app.route('/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    """Delete a car by ID."""
    cars = load_data()
    car = next((c for c in cars if c['id'] == car_id), None)
    if car is None:
        return jsonify({'status': 'error', 'message': 'Car not found'}), 404

    cars.remove(car)
    save_data(cars)
    return jsonify({'status': 'success', 'message': 'Car deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)

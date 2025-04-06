from flask import Flask, request, jsonify, send_from_directory
import os
from SQLfile import Insert_Values, create_user_tables

app = Flask(__name__)

data = {}



@app.route('/')
def serve_html():
    return send_from_directory('.', 'index3.html')

@app.route('/api/insert_data', methods=['POST'])
def insert_data():
    try:
        data = request.get_json()
        print("Received data:", data)

        # Convert dict to list of values in the correct order
        values = [
            data.get("user", "default_user"),
            data.get("feeling"),
            data.get("sleep_duration"),
            data.get("screen"),
            data.get("activity"),
            data.get("hour"),
            data.get("weekday"),
            data.get("sunlight"),
            data.get("safety"),
            data.get("goals"),
            data.get("previous_suggestion")
        ]

        print("Parsed values:", values)

        Insert_Values('data', values)

        return jsonify({"status": "success", "message": "Data stored"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/data')
def show_data():
    global data
    return jsonify(data)

if __name__ == '__main__':
    create_user_tables()
    app.run(debug=True, port=5000)
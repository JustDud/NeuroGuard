from flask import Flask, request, jsonify, send_from_directory
import os
os.system('cls')

app = Flask(__name__)
data = {}

@app.route('/')
def serve_html():
    return send_from_directory('.', 'index3.html')

@app.route('/api/insert_data', methods=['POST'])
def insert_data():
    global data
    try:
        data = request.get_json()
        print("Received data:", data)

        return jsonify({"status": "success", "message": "Data stored"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/data')
def show_data():
    global data
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
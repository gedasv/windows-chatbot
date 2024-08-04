# webapp/app.py
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

BACKEND_URL = "http://localhost:8000"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    response = requests.post(f"{BACKEND_URL}/api/chat", json={"message": message})
    return jsonify(response.json())

@app.route('/history', methods=['GET'])
def history():
    response = requests.get(f"{BACKEND_URL}/api/conversation")
    return jsonify(response.json())

@app.route('/clear', methods=['POST'])
def clear():
    response = requests.post(f"{BACKEND_URL}/api/clear")
    return '', response.status_code

if __name__ == '__main__':
    app.run(debug=True)
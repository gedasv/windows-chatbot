# webapp/app.py
"""
This module implements a Flask web application serving as a frontend for a chat interface.
It communicates with a backend service to handle chat functionality.
"""
from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8000')

@app.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from the user.
    
    This function receives a message from the frontend, forwards it to the backend,
    and returns the backend's response.
    
    :return: A JSON response containing the backend's reply to the chat message.
    """
    message = request.json['message']
    response = requests.post(f"{BACKEND_URL}/api/chat", json={"message": message})
    return jsonify(response.json())

@app.route('/history', methods=['GET'])
def history():
    """
    Retrieve the conversation history from the backend.
    
    :return: A JSON response containing the conversation history.
    """
    include_context = request.args.get('include_context', default='false').lower() == 'true'

    response = requests.get(f"{BACKEND_URL}/api/conversation", params={'include_context': include_context})

    return jsonify(response.json())

@app.route('/clear', methods=['POST'])
def clear():
    """
    Clear the conversation history on the backend.
    
    :return: An empty response with the status code from the backend.
    """
    response = requests.post(f"{BACKEND_URL}/api/clear")
    return '', response.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
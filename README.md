# Window Manufacturing Chatbot

A specialized chatbot for the window manufacturing industry, built with FastAPI and Groq's LLM API.

## Project Overview

Key features:
- FastAPI backend for efficient API handling
- Integration with Groq's LLM API for intelligent responses
- Conversation context management
- Simple web interface for easy interaction
- Dockerized setup for easy deployment

## Project Structure

- **app/**: Contains the core application code.
  - **api/**: Handles API endpoints.
  - **models/**: Defines data models.
  - **services/**: Contains business logic and services.
  - **utils/**: Utility functions and helpers.
  - **main.py**: Entry point of the application.

- **tests/**: Holds test cases.

- **docs/**: Documentation files.

- **webapp/**: Web application components.
  - **templates/**: HTML templates for the web interface.
  - **app.py**: Main file for the web application.


## Setup and Installation

1. Clone the repository:

   `git clone https://github.com/gedasv/windows-chatbot.git`
   
   `cd windows-chatbot`

2. Set up the environment variables:
   Create a .env file in the root directory with the following content:

```
   GROQ_API_KEY=[groq_key_here]
   
   MODEL_NAME=llama3-8b-8192
```

3. Build and run the Docker containers:

   `docker-compose up --build`

This will start both the backend API server and the web application.
You should be able to accesss the web interface in `http://127.0.0.1:5000/` in your browser.

---

To run the services separately for development, create a separate Python env, 
install `requirements.txt` in both app and webapp, and then:

1. Start the backend:

   `uvicorn app.main:app --host 0.0.0.0 --port 8000`

2. In a separate terminal, start the web application:

   `python webapp/app.py`


## API Endpoints

- POST /api/chat: Send a message to the chatbot
- GET /api/conversation: Retrieve the current conversation history with context
- POST /api/clear: Clear the current conversation history


## Testing

There is also a little testing suite. You can run the tests using pytest (when in root folder):

`pytest tests`

## Documentation

You can view the full HTML documentation online at [https://gedasv.github.io/windows-chatbot/](https://gedasv.github.io/windows-chatbot/)

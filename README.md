# Window Manufacturing Chatbot

A specialized chatbot for the window manufacturing industry, built with FastAPI and Groq's LLM API.

## Project Overview

This project implements a chatbot that assists with queries related to window manufacturing. It uses Groq's language model API for generating responses and maintains conversation context for more coherent interactions.

Key features:
- FastAPI backend for efficient API handling
- Integration with Groq's LLM API for intelligent responses
- Conversation context management
- Simple web interface for easy interaction
- Dockerized setup for easy deployment

## Project Structure

Here's how the project is organized:

**app/**: Contains the core application code.
  - **api/**: Handles API endpoints.
  - **models/**: Defines data models.
  - **services/**: Contains business logic and services.
  - **utils/**: Utility functions and helpers.
  - **main.py**: Entry point of the application.
  - **config.py**: Configuration settings.

- **tests/**: Holds test cases for the project.

- **docs/**: Documentation files.

- **webapp/**: Web application components.
  - **templates/**: HTML templates for the web interface.
  - **app.py**: Main file for the web application.

## Setup and Installation

1. Clone the repository:

   git clone https://github.com/yourusername/window_manufacturing_chatbot.git
   cd window_manufacturing_chatbot

2. Set up the environment variables:
   Create a .env file in the root directory with the following content:

   GROQ_API_KEY=[your_groq_api_key_here]
   MODEL_NAME=llama3-8b-8192

3. Build and run the Docker containers:

   docker-compose up --build

This will start both the backend API server and the web application.

## Usage

Once the containers are up and running:

1. Access the web interface at http://localhost:5000 in your browser.
2. Start chatting with the bot about window manufacturing topics.
3. The conversation history and context will be maintained throughout your session.

## API Endpoints

- POST /api/chat: Send a message to the chatbot
- GET /api/conversation: Retrieve the current conversation history
- POST /api/clear: Clear the current conversation history

For detailed API documentation, visit http://localhost:8000/docs after starting the backend server.

## Development

To run the services separately for development:

1. Start the backend:

   uvicorn app.main:app --host 0.0.0.0 --port 8000

2. In a separate terminal, start the web application:

   python webapp/app.py

## Testing

Run the tests using pytest:

pytest

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
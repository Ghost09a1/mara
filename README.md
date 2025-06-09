# Hostable MCP Example

This repository contains a simple Flask application that mimics a basic chat panel similar to the features of [same.new](https://same.new/). The app sends prompts to a locally running Ollama instance (configured with the `qwen3` model) and displays the response in a minimal web interface.

## Features
- Web-based chat panel using Flask
- Integration with Ollama via simple HTTP requests
- Simple HTML interface for sending prompts

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Make sure Ollama is running with the `qwen3` model:
   ```bash
   ollama run qwen3
   ```
3. Run the server:
   ```bash
   python app.py
   ```
4. Open your browser at `http://localhost:5000` to interact with the chat panel.

This example is intentionally minimal and can be extended with additional features such as user authentication, conversation history, and more sophisticated UI elements.

## Docker
To build and run the server in a Docker container:
```bash
docker build -t mcp-app .
docker run -p 5000:5000 mcp-app
```


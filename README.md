# Hostable MCP Example

This repository contains a simple Flask application that forwards prompts to a locally running Ollama instance (configured with the `qwen3` model) and returns the response as JSON.

## Features
- HTTP endpoint using Flask
- Integration with Ollama via simple HTTP requests

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

This example is intentionally minimal and can be extended with additional features such as user authentication, conversation history, and more sophisticated UI elements.

## Docker
To build and run the server in a Docker container:
```bash
docker build -t mcp-app .
docker run -p 5000:5000 mcp-app
```


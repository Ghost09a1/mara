# Hostable MCP Example

This repository contains a simple Flask application that mimics a basic chat panel similar to the features of [same.new](https://same.new/). The app allows you to send prompts to an OpenAI model and view the response in a minimal web interface.

## Features
- Web-based chat panel using Flask
- Integration with OpenAI's API via `openai` library
- Simple HTML interface for sending prompts

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your-key-here
   ```
3. Run the server:
   ```bash
   python app.py
   ```
4. Open your browser at `http://localhost:5000` to interact with the chat panel.

This example is intentionally minimal and can be extended with additional features such as user authentication, conversation history, and more sophisticated UI elements.

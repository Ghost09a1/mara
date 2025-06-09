from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'qwen3')

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'MCP server running'})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    prompt = data.get('prompt', '')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt}
        )
        response.raise_for_status()
        data = response.json()
        reply = data.get('response', '')
        return jsonify({'response': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

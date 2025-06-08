from flask import Flask, request, jsonify, render_template_string
import os
import requests

app = Flask(__name__)

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'qwen3')

TEMPLATE = """
<!doctype html>
<title>MCP Chat</title>
<h1>Simple Chat</h1>
<form action="/chat" method="post">
  <textarea name="prompt" rows="4" cols="50" placeholder="Enter your prompt here..."></textarea><br>
  <input type="submit" value="Send">
</form>
{% if response %}
<h2>Response:</h2>
<pre>{{ response }}</pre>
{% endif %}
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.form.get('prompt', '')
    if not prompt:
        return render_template_string(TEMPLATE, response='No prompt provided.')
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt}
        )
        response.raise_for_status()
        data = response.json()
        reply = data.get("response", "")
    except Exception as e:
        reply = f"Error: {e}"
    return render_template_string(TEMPLATE, response=reply)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

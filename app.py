from flask import Flask, request, jsonify, render_template_string
import os
import openai

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

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
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = completion.choices[0].message['content']
    except Exception as e:
        reply = f"Error: {e}"
    return render_template_string(TEMPLATE, response=reply)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

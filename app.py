from flask import Flask, jsonify
import openai
import os

openai.api_key = os.environ['OPENAPI_API_KEY']
app = Flask(__name__)

# Define an endpoint for discord login


@app.route('/api/discordLogin', methods=['GET'])
def discord_login():
    return jsonify({"user": "test"})

# Define an endpoint for openai


@app.route('/api/openai', methods=['POST'])
def get_openai():
    prompt = "Hello, this is a test, if you can receive this message, just reply: ChatGPT system online."
    response = openai.Completion.create(
        model="text-curie-001", prompt=prompt, temperature=7)
    return jsonify({"openai": "test", "response": response})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

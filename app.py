from flask import Flask, jsonify

app = Flask(__name__)

# Define an endpoint for discord login
@app.route('/api/discordLogin', methods=['GET'])
def discord_login():
    return jsonify({"user": "test"})

# Define an endpoint for openai
@app.route('/api/openai', methods=['POST'])
def get_openai():
    return jsonify({"openai": "test"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

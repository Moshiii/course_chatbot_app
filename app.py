from flask import Flask, jsonify, redirect, request, url_for, session
from flask_login import LoginManager, login_required, login_user, UserMixin
from flask_cors import CORS
from requests_oauthlib import OAuth2Session
import openai
import os
import logging

app = Flask(__name__)
app.secret_key = 'my_secret_key_random_123456789'
login_manager = LoginManager(app)
CORS(app)
# Will defined as env variable
client_id = '1095151304344608770'
client_secret = 'FdXo9-KeXPQBpn2M0R3woU0M49usAwrA'
authorization_base_url = 'https://discord.com/api/oauth2/authorize'
token_url = 'https://discord.com/api/oauth2/token'
api_base_url = 'https://discord.com/api'
scope = 'identify email guilds'
guild_id = '830604066660286464'
openai.api_key = os.environ['OPENAI_API_KEY']
#  disable output buffering in Flask
os.environ['PYTHONUNBUFFERED'] = '1'

class User(UserMixin):
    def __init__(self, id, email, name):
        self.id = id
        self.email = email
        self.name = name

@login_manager.user_loader
def load_user(user_id):
    # Load the user object from the database or other storage
    return User(user_id, session['user_email'], session['user_name'])

# Define an endpoint for discord login
@app.route('/api/discordLogin', methods=['GET'])
def discord_login():
    discord = OAuth2Session(client_id, scope=scope)
    authorization_url, state = discord.authorization_url(authorization_base_url)
    # return redirect(authorization_url)
    response = jsonify({"auth_url": authorization_url})
    return response

# Define an endpoint for discord login callback
@app.route('/api/discordLogin/callback', methods=['GET'])
def discord_callback():
    discord = OAuth2Session(client_id, redirect_uri=request.url, scope=scope)
    # save the access token and other data as needed
    token = discord.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)

    # Store the user's access token in the session for future requests
    session['token'] = token

    # Get the user's guild memberships from the Discord API
    guilds = discord.get(api_base_url + '/users/@me/guilds').json()
    print("get guilds:")
    print(guilds)
    if not any(guild['id'] == guild_id for guild in guilds):
        return 'You are not part of the server, access denied'

    # Retrieve the user's information from the Discord API
    user_info = discord.get(api_base_url + '/users/@me').json()
    user_id = str(user_info['id'])
    user_email = user_info.get('email')
    user_name = user_info.get('username')
    print("get user_info:")
    print(user_info)
    # Load the user object and log the user in
    user = User(user_id, user_email, user_name)
    login_user(user)

    # Store the user's email and name in the session
    session['user_email'] = user_email
    session['user_name'] = user_name

    # Redirect the user to the protected page
    return redirect(url_for('get_home'))

# Define an endpoint for home
@app.route('/', methods=['GET'])
def get_home():
    # Get the user ID from the session and load the user object
    # user_id = session.get('user_id')
    # user = load_user(user_id)

    return "this is home page"

# Define an endpoint for error api
@app.route('/error', methods=['GET'])
def get_error():
    return "this is error page"

# Define an endpoint for discord logout
@app.route('/api/discordLogout')
@login_required
def logout():
    session.clear()
    return redirect('/')

# Define an endpoint for test
@app.route('/api/test', methods=['GET'])
@login_required
def test():
    # Check if the user's access token is in the session
    if 'token' not in session:
        return redirect(url_for('get_error'))
    return jsonify({"TEST": "test"})

# Define an endpoint for openai
@app.route('/api/openai', methods=['POST'])
@login_required
def get_openai():
    prompt = "Hello, this is a test, if you can receive this message, just reply: ChatGPT system online."
    response = openai.Completion.create(
        model="text-curie-001", prompt=prompt, temperature=7)
    return jsonify({"openai": "test", "response": response})


if __name__ == '__main__':
    context = ('cert.pem', 'key.pem')
    app.run(debug=True, host='0.0.0.0', ssl_context=context)

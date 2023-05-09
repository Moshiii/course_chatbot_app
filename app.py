from flask import Flask, jsonify, redirect, request, url_for, session, make_response, request
from functools import wraps
from flask_cors import CORS
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
import openai
import os
import logging
from openai_offline_script import openai_api_test_query
from openai_offline_script import openai_api_test_chat
from openai_offline_script import openai_api_test_query_wiki_context

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# Load the .env file
load_dotenv()

# Will defined as env variable
client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']
authorization_base_url = 'https://discord.com/api/oauth2/authorize'
token_url = 'https://discord.com/api/oauth2/token'
api_base_url = 'https://discord.com/api'
revoke_url = 'https://discord.com/api/oauth2/token/revoke'
scope = 'identify email guilds'
guild_id = '830604066660286464'
openai.api_key = os.environ['OPENAI_API_KEY']
front_end_url = os.environ['FRONT_END_URL']
#  disable output buffering in Flask
os.environ['PYTHONUNBUFFERED'] = '1'

def discord_token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            bearer_token = auth_header[7:]
            discord = OAuth2Session(client_id, token={'access_token': bearer_token, 'token_type': 'Bearer'})
            user_data = discord.get(api_base_url + '/users/@me').json()
            if not 'id' in user_data:
                return jsonify({"error": "Invalid or expired token"}), 401
        else:
            return jsonify({"error": "Authorization header is missing or invalid"}), 401
        return f(*args, **kwargs)
    return wrapper

# Define an endpoint for discord login
@app.route('/api/discordLogin', methods=['GET'])
def discord_login():
    discord = OAuth2Session(client_id, scope=scope)
    authorization_url, state = discord.authorization_url(authorization_base_url)
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

    # Store the user's email and name in the session
    session['user_id'] = user_id
    session['user_email'] = user_email
    session['user_name'] = user_name

    response = redirect(f"{front_end_url}/chat")
    response.set_cookie('access_token', value=token['access_token'])
    return response
   

# Define an endpoint for home
@app.route('/api/home', methods=['GET'])
def get_home():
    return "this is home page"

# Define an endpoint for discord logout
@app.route('/api/discordLogout')
def logout():
    # Revoke the access token
    if 'token' in session:
        discord = OAuth2Session(client_id, token=session['token'])
        print(session['token']['access_token'])
        discord.post(revoke_url, data={'token': session['token']['access_token'],
                                        'client_id': client_id,
                                        'client_secret': client_secret})
        session.clear()
    return jsonify({"message": "logout"})

# Define an endpoint for test
@app.route('/api/test', methods=['GET'])
@discord_token_required
def test():
    return jsonify({"TEST": "test"})

# Define an endpoint for openai
@app.route('/api/openai', methods=['POST'])
@discord_token_required
def chat():
    messages = request.get_json(force=True)
    option = messages[-1]["option"]
    content = messages[-1]["content"]
    if option == "Focus":
        messages = openai_api_test_query.ask_with_wiki_search_on_question_with_context(messages)
    elif option == "Explore":
        messages = openai_api_test_query.ask_with_wiki_search_on_answer_with_context(messages)
    elif "syllabus" in content.lower():
        print("syllabus magic word detected")
        messages = openai_api_test_query.ask_with_syllabus_with_context(messages)
    elif option == "None":
        messages = openai_api_test_query.ask_with_context(messages)
    else:
        messages = openai_api_test_query.ask_with_context(messages)
    # messages = openai_api_test_chat.chat_with_context(messages)
    # messages = openai_api_test_query.ask_with_context(messages)
    # messages = openai_api_test_query.ask_with_wiki_search_on_answer_with_context(messages)
    # messages = openai_api_test_query.ask_with_wiki_search_on_question_with_context(messages)
    # =======================
    # archive
    # =======================
    # messages = openai_api_test_query_wiki_context.ask_with_wiki_search_on_answer_with_context(messages) # problem: tested working but slow
    # messages = openai_api_test_query_wiki_context.ask_with_wiki_search_on_question_with_context(messages) # problem: very general context does not provide good answer
    
    return jsonify(messages)


if __name__ == '__main__':
    context = ('cert.pem', 'key.pem')
    app.run(debug=True, host='0.0.0.0', ssl_context=context)

import os

import openai

openai.api_key = os.environ['OPENAPI_API_KEY']

messages=[
{"role": "system", "content": "You are a helpful assistant."},
{"role": "user", "content": "Who won the world series in 2020?"},
{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
{"role": "user", "content": "Where was it played?"}
]

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",

)
# get message from user
print(response["choices"][0]["message"])
#  append message to messages
messages.append({"role": "assistant", "content": response["choices"][0]["text"]})
import os

import openai

openai.api_key = os.environ['OPENAPI_API_KEY']
prompt = "Hello, this is a test, if you can receive this message, just reply: ChatGPT system online."
response = openai.Completion.create(
        model="text-curie-001", prompt=prompt, temperature=0.0)
print(response['choices'][0]['text'])
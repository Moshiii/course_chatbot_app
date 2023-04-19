import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']

def chat_with_context(user_message,messages):
    messages.append({"role": "user", "content": user_message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    answer = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": answer})
    return answer,messages

messages=[
{"role": "system", "content": "You are a helpful assistant."}
]


question = "Who won the world series in 2020?"
print(question)
answer,messages = chat_with_context(question,messages)
print(answer)


question = "Where was it played?"
print(question)
answer,messages = chat_with_context(question,messages)
print(answer)

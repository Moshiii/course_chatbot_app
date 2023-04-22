import os
import openai

openai.api_key = os.environ['OPENAI_API_KEY']

# def chat_with_context(user_message,messages):
#     messages.append({"role": "user", "content": user_message})
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#     )
#     answer = response["choices"][0]["message"]["content"]
#     messages.append({"role": "assistant", "content": answer})
#     return answer,messages

def chat_with_context(messages):
    if messages[-1]["role"]!="user":
        print("last message is not from user")
        return None
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )
    answer = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": answer})
    return messages


messages=[
{"role": "system", "content": "You are a helpful assistant."}
]


question = "Who won the world series in 2020?"
messages.append({"role": "user", "content": question})
messages = chat_with_context(messages)
print(messages[-1]["content"])


question = "Where was it played?"
messages.append({"role": "user", "content": question})
messages = chat_with_context(messages)
print(messages[-1]["content"])


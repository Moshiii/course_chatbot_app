import os
import openai
from dotenv import load_dotenv
openai.api_key = os.environ['OPENAI_API_KEY']
# Load the .env file
load_dotenv()
def chat_with_context(messages):
    #if last messgae is not from user, return None
    if messages[-1]["role"]!="user":
        print("last message is not from user")
        return None
    #remove option attribute from dict
    for message in messages:
        message.pop("option", None)
        
    
    #====================================
    # openai API call
    #====================================
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    answer = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": answer})
    return messages

if __name__ == "__main__":
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
    print(messages)




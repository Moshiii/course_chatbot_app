import os
import numpy as np
import openai
import json
from openai_offline_script import openai_api_test_key_word_extraction
from openai_offline_script import wikipedia_api_test


from dotenv import load_dotenv
# Load the .env file
load_dotenv()

openai.api_key = os.environ['OPENAI_API_KEY']

def ask_with_wiki_search_on_question(query: str):

    result_list = openai_api_test_key_word_extraction.extract_key_word_list(
        query)
    context = {}
    links = {}
    for x in result_list:
        title, url, summary, references = wikipedia_api_test.search_wiki(x)
        print("link: ", url)
        # print(title)
        # print(summary)
        context[title] = summary
        links[title] = url

    ctx = ""
    for key in context.keys():
        ctx = ctx + " keyword: " + key + " keyword explain: " + context[key]

    prompt = "".join([
        u"Answer the question with consideration of the following context, if context is irrelevent, answer based on your own understanding:\n\n"
        u"context:" + ctx + u"\n\n"
        u"Q:"+query+u"\n\n"
        u"A:"])

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    answer = completion.choices[0].message.content
    
    answer+="\n\n"
    for key in links.keys():
        answer+="\n"+key+": "+links[key]

    return answer


def ask_with_wiki_search_on_answer(query: str):


    prompt = query

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])

    answer = completion.choices[0].message.content

    result_list = openai_api_test_key_word_extraction.extract_key_word_list(
        answer)
    print(result_list)
    context = {}
    links = {}
    for x in result_list:
        title, url, summary, references = wikipedia_api_test.search_wiki(x)
        print("link: ", url)
        # print(title)
        # print(summary)
        context[title] = url
        links[title] = url
    # append list of links after the anwser
    answer+="\n\n"
    for key in links.keys():
        answer+="\n"+key+": "+links[key]

    return answer
    
def ask_with_wiki_search_on_question_with_context(messages: str) -> str:

    user_query  = messages[-1]["content"]
    answer = ask_with_wiki_search_on_question(user_query)
    messages.append({"role": "assistant", "content": answer})

    
def ask_with_wiki_search_on_answer_with_context(messages: str) -> str:

    user_query  = messages[-1]["content"]
    answer = ask_with_wiki_search_on_answer(user_query)
    messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    query = "what is the loss function of a recurrent neural network?"
    answer = ask_with_wiki_search_on_question(query)
    # answer = ask_with_wiki_search_on_answer(query)
    print(answer)
import os
import numpy as np
import openai
import json
from dotenv import load_dotenv
from openai_offline_script import openai_api_test_key_word_extraction
from openai_offline_script import wikipedia_api_test
# Load the .env file
load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']
EMBEDDING_MODEL = "text-embedding-ada-002"
CONTEXT_TOKEN_LIMIT = 5000


def get_embedding(text: str, model: str = EMBEDDING_MODEL) -> list[float]:
    result = openai.Embedding.create(
        model=model,
        input=text
    )
    return result["data"][0]["embedding"]


def vector_similarity(x: list[float], y: list[float]) -> float:
    return np.dot(np.array(x), np.array(y))


def order_document_sections_by_query_similarity(query: str, embeddings) -> list[(float, (str, str))]:
    query_embedding = get_embedding(query)
    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in enumerate(embeddings)
    ], reverse=True, key=lambda x: x[0])
    return document_similarities


def ask_with_context(messages: str) -> str:

    embeddings = []
    sources = []
    filenames = []
    pageindex = []
    with open('content_update.json', 'r') as f:
        content = json.load(f)

    for source in content.keys():
        for idx, x in enumerate(content[source]):
            embeddings.append(x['embedding'])
            sources.append(x['text'])
            filenames.append(source)
            pageindex.append(idx)

    user_query = messages[-1]["content"]
    answer = ask(user_query, embeddings, sources, filenames, pageindex)
    messages.append({"role": "assistant", "content": answer})
    return messages

def ask_with_syllabus_with_context(messages: str) -> str:
    user_query = messages[-1]["content"]
    answer = ask_syllabus(user_query)
    messages.append({"role": "assistant", "content": answer})
    return messages

def ask_syllabus(question: str):
    file_path = "MECH3202_outline_S23.txt"
    with open(file_path, 'r', encoding='ISO-8859-1') as f:
        content = f.read()
    prompt='this is the syllubus for a course. please read and answer the following questions. Please think carefully'
    prompt += content   
    prompt += question

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    return completion.choices[0].message.content

def ask(question: str, embeddings, sources, filenames, pageindex):
    ordered_candidates = order_document_sections_by_query_similarity(
        question, embeddings)
    ctx = ""
    for candi in ordered_candidates:
        next = ctx + " " + "file name: "+filenames[candi[1]]+" page index: "+str(
            pageindex[candi[1]])+" file content:" + sources[candi[1]]
        if len(next) > CONTEXT_TOKEN_LIMIT:
            break
        ctx = next
    if len(ctx) == 0:
        return ""
    prompt = "".join([
        u"Answer the question based on the following context. If context is irrelevent, answer based on your own understanding:\n\n"
        u"context:" + ctx + u"\n\n"
        u"Q:"+question+u"\n\n"
        u"A:"])

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    return completion.choices[0].message.content


def ask_with_wiki_search_on_answer_with_context(messages):

    embeddings = []
    sources = []
    filenames = []
    pageindex = []
    with open('content_update.json', 'r') as f:
        content = json.load(f)

    for source in content.keys():
        for idx, x in enumerate(content[source]):
            embeddings.append(x['embedding'])
            sources.append(x['text'])
            filenames.append(source)
            pageindex.append(idx)

    user_query = messages[-1]["content"]
    answer = ask(user_query, embeddings, sources, filenames, pageindex)

    result_list = openai_api_test_key_word_extraction.extract_key_word_list(
        answer)
    context = {}
    links = {}
    for x in result_list[:3]:
        title, url, summary, references = wikipedia_api_test.search_wiki_first_only(
            x)
        context[title] = url
        links[title] = url
    answer += "\n\n"
    for key in links.keys():
        answer += "\n"+key+": "+links[key]

    messages.append({"role": "assistant", "content": answer})
    return messages


def ask_with_wiki_search_on_question_with_context(messages):

    embeddings = []
    sources = []
    filenames = []
    pageindex = []
    with open('content_update.json', 'r') as f:
        content = json.load(f)

    for source in content.keys():
        for idx, x in enumerate(content[source]):
            embeddings.append(x['embedding'])
            sources.append(x['text'])
            filenames.append(source)
            pageindex.append(idx)

    user_query = messages[-1]["content"]
    answer = ask(user_query, embeddings, sources, filenames, pageindex)

    result_list = openai_api_test_key_word_extraction.extract_key_word_list(
        user_query)
    context = {}
    links = {}
    for x in result_list:
        title, url, summary, references = wikipedia_api_test.search_wiki(x)
        context[title] = summary
        links[title] = url

    messages.append({"role": "assistant", "content": answer})
    return messages


if __name__ == "__main__":
    embeddings = []
    sources = []
    filenames = []
    pageindex = []
    with open('content_update.json', 'r') as f:
        content = json.load(f)

    for source in content.keys():
        for idx, x in enumerate(content[source]):
            embeddings.append(x['embedding'])
            sources.append(x['text'])
            filenames.append(source)
            pageindex.append(idx)

    result = ask("What is cost function? can you give me an example",
                 embeddings, sources, filenames, pageindex)

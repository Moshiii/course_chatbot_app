import os
import numpy as np
import openai
import json
from dotenv import load_dotenv
# Load the .env file
load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']
EMBEDDING_MODEL = "text-embedding-ada-002"
CONTEXT_TOKEN_LIMIT = 3000


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
    # print("document_similarities",document_similarities)
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


    user_query  = messages[-1]["content"]
    answer = ask(user_query,embeddings, sources, filenames, pageindex)
    messages.append({"role": "assistant", "content": answer})

def ask(question: str, embeddings, sources, filenames, pageindex):
    ordered_candidates = order_document_sections_by_query_similarity(
        question, embeddings)
    ctx = ""
    for candi in ordered_candidates:
        next = ctx + " " +"file name: "+filenames[candi[1]]+" page index: "+str(pageindex[candi[1]])+" file content:"+ sources[candi[1]]
        if len(next) > CONTEXT_TOKEN_LIMIT:
            break
        print("next",next)
        ctx = next
    if len(ctx) == 0:
        return ""
    prompt = "".join([
        u"Answer the question based on the following context:\n\n"
        u"context:" + ctx + u"\n\n"
        u"Q:"+question+u"\n\n"
        u"A:"])

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
    return completion.choices[0].message.content


if __name__ == "__main__":
    embeddings = []
    sources = []
    filenames = []
    pageindex = []
    with open('content_update.json', 'r') as f:
        content = json.load(f)

    for source in content.keys():
        for idx, x in enumerate(content[source]):
            print(x.keys())
            embeddings.append(x['embedding'])
            sources.append(x['text'])
            filenames.append(source)
            pageindex.append(idx)

    result = ask("What is cost function? can you give me an example", embeddings, sources, filenames, pageindex)
    print(result)
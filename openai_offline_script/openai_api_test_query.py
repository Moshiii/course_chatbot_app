import os
import numpy as np
import openai
import json

openai.api_key = os.environ['OPENAPI_API_KEY']
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
    print("document_similarities",document_similarities)
    return document_similarities


def ask(question: str, embeddings, sources):
    ordered_candidates = order_document_sections_by_query_similarity(
        question, embeddings)
    ctx = ""
    for candi in ordered_candidates:
        next = ctx + " " + sources[candi[1]]
        if len(next) > CONTEXT_TOKEN_LIMIT:
            break
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
    return [prompt, completion.choices[0].message.content]


embeddings = []
sources = []
with open('content_update.json', 'r') as f:
    content = json.load(f)

for source in content.keys():
    for idx, x in enumerate(content[source]):
        print(x.keys())
        embeddings.append(x['embedding'])
        sources.append(x['text'])

result = ask("What is cost function? can you give me an example", embeddings, sources)
print(result)
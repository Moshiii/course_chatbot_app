import os
import numpy as np
import openai
import json

openai.api_key = os.environ['OPENAI_API_KEY']
EMBEDDING_MODEL = "text-embedding-ada-002"
CONTEXT_TOKEN_LIMIT = 1024


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



#===================================================================================================
# main
#===================================================================================================
embeddings = []
sources = []
with open('content.json', 'r') as f:
    content = json.load(f)

# with open('content_update.json', 'r') as f:
#     content = json.load(f)

for source in content.keys():
    if source=="main_notes.pdf":
        content[source] = content[source][9:12]
    for idx, x in enumerate(content[source]):
        content[source][idx]["embedding"] = get_embedding(source)

# save json file
with open('content_update.json', 'w') as f:
    json.dump(content, f)

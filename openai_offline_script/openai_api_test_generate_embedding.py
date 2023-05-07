import os
import numpy as np
import openai
import json
from dotenv import load_dotenv
import tiktoken

# Load the .env file
load_dotenv()
# openai.api_key = os.environ['OPENAI_API_KEY']
openai.api_key = "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"
EMBEDDING_MODEL = "text-embedding-ada-002"
CONTEXT_TOKEN_LIMIT = 1024

def get_token_count(string,model):
    # print("string: ", string)
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_embedding(text: str, model: str = EMBEDDING_MODEL) -> list[float]:
    result = openai.Embedding.create(
        model=model,
        input=text
    )
    return result["data"][0]["embedding"]


def get_embedding_quote(text: str, model: str = EMBEDDING_MODEL) -> list[float]:
    token_len = get_token_count(text,model)
    print("token_len: ", token_len)



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
    # if source=="main_notes.pdf":
    #     content[source] = content[source][9:12]
    for idx, x in enumerate(content[source]):
        content[source][idx]["embedding"] = get_embedding(content[source][idx]["text"])
        # get_embedding_quote(content[source][idx]["text"],"gpt-3.5-turbo")

# save json file
with open('content_update.json', 'w') as f:
    json.dump(content, f)

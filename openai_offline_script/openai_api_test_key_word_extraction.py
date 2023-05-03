import os
import openai
from dotenv import load_dotenv
# Load the .env file
load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']
EXTRACTION_MODEL = "text-davinci-001"
TOKEN_LIMIT = 1000


def extract_key_word_list(query: str) -> list[float]:

    prompt = 'please extract the keywords from the following text seperated by comma: '
    prompt += query

    response = openai.Completion.create(
        model=EXTRACTION_MODEL, prompt=prompt, temperature=0.1, max_tokens=TOKEN_LIMIT)
    
    result = response['choices'][0]['text']
    result = result.split(',')
    result = [x.strip() for x in result]
    return result


if __name__ == "__main__":
    query = "what is the loss function of a recurrent neural network?"
    result_list = extract_key_word_list(query)
    print(result_list)

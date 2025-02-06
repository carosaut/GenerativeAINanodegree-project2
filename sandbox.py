import pandas as pd
import requests
from openai import OpenAI
import tiktoken

from api_key import openai_key, api_base

embed_model = "text-embedding-ada-002"
chat_model = "gpt-3.5-turbo-instruct"

df = pd.DataFrame()

# get text from wikipidia api
params = {
    "action": "query", 
    "prop": "extracts",
    "exlimit": 1,
    "titles": "The_Game_Awards_2024",
    "explaintext": 1,
    "formatversion": 2,
    "format": "json"
}
response = requests.get("https://en.wikipedia.org/w/api.php", params=params)
response_dict = response.json()

# clean data
wiki_text = response_dict["query"]["pages"][0]["extract"].split("\n")
filtered_lines = filter(lambda x: x != '' and not x.startswith('=='), wiki_text)
cleaned_text = list(filtered_lines)

# put in dataframe and save as csv file
df['text'] = cleaned_text


client = OpenAI(
    base_url = api_base,
    api_key = "your api key"
)

def embedding_generator(client, text):
    response = client.embeddings.create(
        model=embed_model,
        input=text
    )
    return response


embeddings = embedding_generator(client, df['text'].tolist())

print(embeddings.data[0].embedding)

full_embeddings_list = [i.embedding for i in embeddings.data]

df["embeddings"] = full_embeddings_list
   
   # Taken from Retrieval Augmented Generation lesson
df.to_csv("The_Game_Awards_2024.csv")


#fetch data from csv
df = pd.read_csv("The_Game_Awards_2024.csv", index_col=0)

prompt_template = '''
Answer the question based on the context below, and if the question
can't be answered based on the context, say "I don't know"

Context: 

{}

---

Question: {}
Answer:'''


tokeniser = tiktoken.get_encoding("cl100k_base")

def ai_generator(user_prompt):
    result = client.completions.create(
            model=chat_model,
            prompt=user_prompt,
            max_tokens=32,
            temperature=0
        )

    print(result.choices[0].text.strip())

def format_prompt(prompt, context):
    formatted_prompt = prompt_template.format('\n\n'.join(context), prompt)
    return formatted_prompt
    

def chat(user_prompt, context):
    try:
        complete_prompt = format_prompt(user_prompt, context)
        result = ai_generator(complete_prompt)

        return result
    
    except Exception as ex:
        return str(ex)

print(chat("Who won the game awards 2024?", df["text"]))

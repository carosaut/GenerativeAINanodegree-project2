import pandas as pd
import requests

df = pd.DataFrame()
embeddings_model = 

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
df.to_csv("The_Game_Awards_2024.csv")





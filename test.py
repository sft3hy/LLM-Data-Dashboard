import requests
import os
from helpers.model_caller import call_model
from config import *

api_key = os.environ.get("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# response = requests.get(url, headers=headers)

# for llm in response.json()['data']:
#     print(llm['id'])

response = call_model("llama-3.1-70b-versatile", 'What is the meaning of life?', normal_sys_prompt)
print(response)
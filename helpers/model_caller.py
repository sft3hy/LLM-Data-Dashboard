import os
from openai import OpenAI
import json
import re
from groq import Groq
from config import GROQ_MODELS, get_now, GROQ_API_KEY, AZURE_API_KEY
from datetime import datetime


groq_client = Groq(
    api_key=GROQ_API_KEY,
)

openai_models = ['gpt-4o', 'gpt-4o-mini']
openai_token = AZURE_API_KEY
openai_endpoint = "https://models.inference.ai.azure.com"
openai_client = OpenAI(
    base_url=openai_endpoint,
    api_key=openai_token,
)

def decrement(model_name: str):
    counter_file = 'helpers/gpt_counter.json'
    counts = json.load(open(counter_file, 'r'))
    if model_name in counts.keys():
        counts[model_name] -= 1
        json.dump(counts, open(counter_file, 'w'))

def call_model(model_name: str, gpt_request: str, system_prompt: str, role="user"):
    gpt_response = ""
    client = ""
    if model_name in openai_models:
        client = openai_client
    elif model_name in GROQ_MODELS:
        client = groq_client
    else:
        print("Invalid model name")
        return None
    response = client.chat.completions.create(
        messages=[
            system_prompt,
            {
                "role": role,
                "content": gpt_request,
            }
        ],
        temperature=1.0,
        top_p=1.0,
        max_tokens=3000,
        model=model_name
    )
    gpt_response = response.choices[0].message.content

    with open('data/prompt_history.log', 'a') as f:
        cleaned = re.sub(r'\s+', ' ', gpt_request).strip()
        f.write(f"\nUSER REQUEST:\n{cleaned}\nUsing model: {model_name}\nAt {get_now()}\nMODEL RESPONSE: {gpt_response}\n")
    return gpt_response


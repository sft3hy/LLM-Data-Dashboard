import os
from openai import OpenAI

token = os.environ["GITHUB_ACCESS_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def generate_streamlit(gpt_request: str):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a helpful dashboard creating assistant.
                Your job is to write streamlit code based on a user's input.
                You will be given a sample of their uploaded data, the filename(s) and filepath(s) and their request
                of what insights they want to know about their data. You will output
                only the streamlit code that will visualize their requested dashboard insights BASED ON THEIR FILES.
                "Output the code without any formatting or backticks.""",
            },
            {
                "role": "user",
                "content": gpt_request,
            }
        ],
        temperature=1.0,
        top_p=1.0,
        max_tokens=1000,
        model=model_name
    )
    gpt_response = response.choices[0].message.content
    return gpt_response
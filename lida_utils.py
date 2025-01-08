from helpers.model_caller import call_model
from config import GROQ_LIDA_MODEL, AZURE_LIDA_MODEL, get_now, AZURE_API_KEY, GROQ_API_KEY
import os
from typing import Union, List, Dict
from lida import Manager
from llmx import TextGenerationConfig, TextGenerationResponse, Message
from openai import AzureOpenAI
from groq import Groq


def get_models_maxtoken_dict(models_list):
    if not models_list:
        return {}

    models_dict = {}
    for model in models_list:
        if "model" in model and "parameters" in model["model"]:
            details = model["model"]["parameters"]
            models_dict[details["model"]] = model["max_tokens"]
    return models_dict

class CustomTextGenerator():
    def __init__(
        self,
        api_key: str = GROQ_API_KEY,
        provider: str = "groq",
        organization: str = None,
        api_type: str = None,
        api_version: str = None,
        azure_endpoint: str = "https://models.inference.ai.azure.com",
        model: str = None,
        models: Dict = None,
    ):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY", None)

        if self.api_key is None:
            raise ValueError(
                "Groq API key is not set. Please set the GROQ_API_KEY environment variable."
            )

        self.client_args = {
            "api_key": self.api_key,
            "organization": organization,
            "api_version": "2024-10-21",
            "azure_endpoint": azure_endpoint,
        }
        # remove keys with None values
        self.client_args = {k: v for k,
                            v in self.client_args.items() if v is not None}

        if api_type:
            if api_type == "azure":
                self.client = AzureOpenAI(**self.client_args)
            else:
                raise ValueError(f"Unknown api_type: {api_type}")
        else:
            self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"),)

        self.model = model or "llama3-70b-8192"
        self.model_max_token_dict = get_models_maxtoken_dict(models)
        self.provider = provider

    def generate(
        self,
        messages: Union[List[dict], str],
        config: TextGenerationConfig = TextGenerationConfig(),
        **kwargs,
    ) -> TextGenerationResponse:
        model = config.model or self.model

        groq_config = {
            "model": model,
            "temperature": config.temperature,
            "top_p": config.top_p,
            "frequency_penalty": config.frequency_penalty,
            "presence_penalty": config.presence_penalty,
            "n": 1,
            "messages": messages,
        }

        self.model = model

        groq_response = self.client.chat.completions.create(**groq_config)

        response = TextGenerationResponse(
            text=[Message(**x.message.model_dump())
                  for x in groq_response.choices],
            logprobs=[],
            usage=str(groq_response.usage),
            config=groq_config,
        )
        with open('data/prompt_history.log', 'a') as f:
            f.write(f"\nUSER REQUEST:\n{messages}\nUsing model: {model}\nAt {get_now()}\nMODEL RESPONSE: {response}\n")
        return response
    
    def count_tokens():
        return 0


# Instantiate your custom generator
groq_generator = CustomTextGenerator(model=GROQ_LIDA_MODEL,)
azure_generator = CustomTextGenerator(model=AZURE_LIDA_MODEL,
                                    api_type="azure",
                                    api_key=AZURE_API_KEY,
                                    )

# To use, ininitialize lida like the following:
# groq_lida = Manager(text_gen=groq_generator)
# azure_lida = Manager(text_gen=azure_generator)
# textgen_config = TextGenerationConfig(
#     n=1,
#     temperature=0.5, # choose a value between 0 and 1
#     model="llama3-70b-8192",)

# # **** lida.summarize *****
# summary = groq_lida.summarize(
#     "path/to/dataset.csv", # csv or json
#     summary_method="llm", # choose from ["llm","columns","default"]
#     textgen_config=textgen_config)
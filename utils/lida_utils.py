from config import get_now, GROQ_MODELS, GROQ_API_KEY, GOOGLE_API_KEY, GOOGLE_MODELS
from typing import Union, List, Dict
from lida import Manager
from llmx import TextGenerationConfig, TextGenerationResponse, Message
from openai import AzureOpenAI, OpenAI
from groq import Groq
from utils.model_call_tracker import update_model_count


def get_models_maxtoken_dict(models_list):
    if not models_list:
        return {}

    models_dict = {}
    for model in models_list:
        if "model" in model and "parameters" in model["model"]:
            details = model["model"]["parameters"]
            models_dict[details["model"]] = model["max_tokens"]
    return models_dict


class CustomTextGenerator:
    def __init__(
        self,
        api_key: str = GROQ_API_KEY,
        provider: str = "groq",
        organization: str = None,
        api_type: str = None,
        api_version: str = None,
        api_endpoint: str = "https://models.inference.ai.azure.com",
        model: str = None,
        models: Dict = None,
    ):
        self.api_key = api_key or GROQ_API_KEY

        if self.api_key is None:
            raise ValueError(
                "Groq API key is not set. Please set the GROQ_API_KEY environment variable."
            )

        self.client_args = {
            "api_key": self.api_key,
            "organization": organization,
            "api_version": "2024-10-21",
            "azure_endpoint": "https://models.inference.ai.azure.com",
        }
        # remove keys with None values
        self.client_args = {k: v for k, v in self.client_args.items() if v is not None}

        # must pick an api type
        if api_type == "groq":
            self.client = Groq(
                api_key=GROQ_API_KEY,
            )
        elif api_type == "azure":
            self.client = AzureOpenAI(**self.client_args)
        elif api_type == "google":
            self.client = OpenAI(
                api_key=GOOGLE_API_KEY,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            )
        else:
            raise ValueError(f"Unknown api_type: {api_type}")

        self.model = model
        self.model_max_token_dict = get_models_maxtoken_dict(models)
        self.provider = provider

    def generate(
        self,
        messages: Union[List[dict], str],
        config: TextGenerationConfig = TextGenerationConfig(),
        **kwargs,
    ) -> TextGenerationResponse:
        model = config.model or self.model

        model_config = {
            "model": model,
            "temperature": config.temperature,
            "top_p": config.top_p,
            "n": config.n,
            "messages": messages,
        }
        if model not in GOOGLE_MODELS:
            model_config["frequency_penalty"] = config.frequency_penalty
            model_config["presence_penalty"] = config.presence_penalty
        if model in GROQ_MODELS:
            model_config["n"] = 1

        self.model = model

        model_response = self.client.chat.completions.create(**model_config)

        response = TextGenerationResponse(
            text=[Message(**x.message.model_dump()) for x in model_response.choices],
            logprobs=[],
            usage=str(model_response.usage),
            config=model_config,
        )
        with open("data/prompt_history.log", "a") as f:
            f.write(
                f"\nUSER REQUEST:\n{messages}\nUsing model: {model}\nAt {get_now()}\nMODEL RESPONSE: {response}\n"
            )
        update_model_count(model, increment=True)
        return response

    def count_tokens():
        return 0


# To use, ininitialize lida like the following:
# Instantiate your custom generator
# groq_generator = CustomTextGenerator(model="llama-3.3-70b-versatile",)
# azure_generator = CustomTextGenerator(model="gpt-4o-mini",
#                                     api_type="azure",
#                                     )
# google_generator = CustomTextGenerator(model="gemini-2.0-flash-exp",
#                                     api_type="google",
#                                     )
# groq_lida = Manager(text_gen=groq_generator)
# azure_lida = Manager(text_gen=azure_generator)
# textgen_config = TextGenerationConfig(
#     n=1,
#     temperature=0.5, # choose a value between 0 and 1
#     model="llama-3.3-70b-versatile",)

# # **** lida.summarize *****
# summary = groq_lida.summarize(
#     "path/to/dataset.csv", # csv or json
#     summary_method="llm", # choose from ["llm","columns","default"]
#     textgen_config=textgen_config)

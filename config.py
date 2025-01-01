streamlit_sys_prompt = {
                    "role": "system",
                    "content": """You are a helpful dashboard creating assistant.
                    Your job is to write streamlit code based on a user's input.
                    You will be given a sample of their uploaded data, the filename(s) and filepath(s) and their request
                    of what insights they want to know about their data. You will output
                    only the streamlit code that will visualize their requested dashboard insights BASED ON THEIR FILES.
                    Output the code without any formatting or backticks.""",
                }

code_corrector_sys_prompt = {
    "role": "system",
    "content": """You are a helpful code corrector assistant. You will be
    supplied with source streamlit code, and an error that it generates. Your job is to correct the code
    so that it no longer throws the error. You will also be given additional context about what the code is trying to do.
    Output only the corrected code without any formatting or backticks. 
    """
}

code_refiner_sys_prompt = {
    "role": "system",
    "content": """You are a helpful code refiner assistant. You will be
    supplied with source streamlit code, and a description of what the code is trying to do. Your job is to refine the code
    so that it accomplishes what the user asks for. You will be given the source code snippet, and context of how the user wants to refine it.
    Output only the refined code without any formatting or backticks. Do not explain the code, just output
    the full streamlit app.
    """
}

normal_sys_prompt = {
    "role": "system",
    "content": """You answer questions concisely"""
}

MODEL_LIMITS = [
    {"Model": "gpt-4o", "Daily Calls": 50},
    {"Model": "gpt-4o-mini", "Daily Calls": 150},
    {"Model": "llama-3.3-70b-versatile", "Daily Calls": 1000},
    {"Model": "llama-3.3-70b-specdec", "Daily Calls": 1000},
    {"Model": "llama-3.1-70b-versatile", "Daily Calls": 1000},
    {"Model": "llama3-70b-8192", "Daily Calls": 14400},
    {"Model": "llama3-groq-70b-8192-tool-use-preview", "Daily Calls": 14400},
    {"Model": "gemma2-9b-it", "Daily Calls": 14400},
    {"Model": "mixtral-8x7b-32768", "Daily Calls": 14400},
]

GROQ_MODELS = ["llama-3.3-70b-versatile",
               "llama-3.3-70b-specdec",
               "llama-3.1-70b-versatile",
               "llama3-70b-8192",
               "llama3-groq-70b-8192-tool-use-preview", 
               "gemma2-9b-it",
               "mixtral-8x7b-32768"
               ]


"""
llama-3.2-90b-vision-preview
llama-guard-3-8b
"""

CODE_CORRECTION_TRIES = 5
CODE_CORRECTOR_MODEL = "llama3-70b-8192"
CODE_REFINER_MODEL = "llama3-70b-8192"

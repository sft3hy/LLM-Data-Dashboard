import json
from utils.misc import choose_text_generator, parse_model_response
from utils.lida_utils import TextGenerationConfig


def decrement(model_name: str):
    counter_file = 'helpers/gpt_counter.json'
    counts = json.load(open(counter_file, 'r'))
    if model_name in counts.keys():
        counts[model_name] -= 1
        json.dump(counts, open(counter_file, 'w'))

def call_model(model_name: str, gpt_request: str, system_prompt: str, role="user", temperature=0.2):

    textgen_config = TextGenerationConfig(
        n=1,
        temperature=temperature,
        model=model_name,)

    text_gen = choose_text_generator(model_name)
    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": gpt_request}]

    result = text_gen.generate(messages=messages, config=textgen_config)

    # response = call_model(model_name=selected_model, gpt_request=formatted, system_prompt=streamlit_sys_prompt)
    response = parse_model_response(result)
    return response
    
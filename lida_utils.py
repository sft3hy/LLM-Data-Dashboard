import streamlit as st
from lida.datamodel import Goal
from helpers.model_caller import call_model
from config import summarizer_sys_prompt, LIDA_MODEL

class giveText:
    def __init__(self):
        self.text = []
        self.usage = ""
    def setText(self, text):
        self.text = [{"content": text}]
    
class CustomTextGenerator:
    def __init__(self, system_prompt=summarizer_sys_prompt, provider="custom", model_name="llama-3.3-70b-versatile"):
        self.model_name = model_name
        self.provider = provider  # Adding the provider attribute
        self.system_prompt = system_prompt

    def generate(self, messages, config=""):
        for message in messages:
            role = ''
            content = ''
            sys = self.system_prompt
            if 'role' in message.keys() and 'content' in message.keys():
                role = message['role']
                if message['role'] == 'system':
                    sys = message['content']
                else:
                    content = message['content']
        response = call_model(
            model_name=self.model_name,
            gpt_request=content,
            role=role,
            system_prompt=sys
        )
        # response = "{'ayo'}"
        print('RESPONSE', response)
        r = giveText()
        r.setText(response)
        return r
    

# Instantiate your custom generator
custom_gen = CustomTextGenerator(
    model_name=LIDA_MODEL,
)

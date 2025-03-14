from utils.model_caller import call_model
from config import code_corrector_sys_prompt, CODE_CORRECTION_TRIES, CODE_CORRECTOR_MODEL, code_refiner_sys_prompt, CODE_REFINER_MODEL, get_now
import streamlit as st
from utils.message_utils import set_file_messages, get_file_messages
from utils.misc import extract_message, clean_set_page_config
import contextlib
import io
import traceback
import time
from datetime import datetime

def correct_code(code_snippet: str, extra_context: str, file_name: str):
    current_try = 1
    corrected = clean_set_page_config(extract_message(code_snippet))
    first_try = "The generated code was good but not perfect. Llama3 is now reviewing the code for any errors."
    while current_try <= CODE_CORRECTION_TRIES:
        try:
            # Capture output and error streams
            output_stream = io.StringIO()
            error_stream = io.StringIO()
            
            with contextlib.redirect_stdout(output_stream), contextlib.redirect_stderr(error_stream):
                # Isolated execution environment
                exec_environment = {}
                with contextlib.redirect_stdout(None):
                    exec(corrected, exec_environment)
                    
        except Exception as e:
            # Log the error and the captured output
            print(f"ERROR at {get_now()} in helpers.code_editor.22 - {e}")
            formatted=f"This is the code: {corrected}\nThis is the error: {e}\nThis is the context: {extra_context}\nPlease output the corrected code"
            if current_try == 1:
                msg = st.toast(first_try)
            msg.toast(f"Error correction {current_try}/{CODE_CORRECTION_TRIES} running...")
            time.sleep(0.5)
            corrected = clean_set_page_config(extract_message(call_model(CODE_CORRECTOR_MODEL, formatted, code_corrector_sys_prompt)))
            if current_try == CODE_CORRECTION_TRIES:
                st.info(f"Too many errors, try passing this error code as your next prompt:\n{e}")
        current_try += 1
    if file_name != "":
        old_messages = get_file_messages(file_name)
        old_clean_messages = old_messages[:-1]
        last_message = old_messages[-1]
        last_message['assistant_code'] = corrected
        new_messages = old_clean_messages + [last_message]
        set_file_messages(file_name, new_messages)
    return corrected

def code_refiner(code_snippet: str, extra_context: str, model: str):
    """
    Refines the code snippet using a user selected model for code refinement.
    
    Args:
        code_snippet (str): The code snippet to refine.
        extra_context (str): Additional context to provide to the model.
    
    Returns:
        str: The refined code snippet.
    """
    whole_prompt = f"Original code: {code_snippet}\n' User request: {extra_context}"
    refined_code = extract_message(call_model(model, whole_prompt, code_refiner_sys_prompt))
    
    return refined_code
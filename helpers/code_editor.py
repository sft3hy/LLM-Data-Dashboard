from helpers.model_caller import call_model
from config import code_corrector_sys_prompt, CODE_CORRECTION_TRIES, CODE_CORRECTOR_MODEL, code_refiner_sys_prompt, CODE_REFINER_MODEL
import streamlit as st
from helpers.misc import extract_message
import contextlib
import io
import traceback

def correct_code(code_snippet: str, extra_context: str):
    current_try = 1
    corrected = extract_message(code_snippet)
    first_try = "The generated code was good but not perfect. Llama3 is now reviewing the code for any errors."
    while current_try <= CODE_CORRECTION_TRIES:
        try:
            # Capture output and error streams
            output_stream = io.StringIO()
            error_stream = io.StringIO()
            
            with contextlib.redirect_stdout(output_stream), contextlib.redirect_stderr(error_stream):
                # Isolated execution environment
                exec_environment = {}
                exec(corrected, exec_environment)
            
            return corrected  # If execution succeeds, return corrected code
        
        except Exception as e:
            # Log the error and the captured output
            detailed_error = traceback.format_exc()
            print(e)
            formatted=f"This is the code: {corrected}\nThis is the error: {detailed_error}\nThis is the context: {extra_context}\nPlease output the corrected code"
            if current_try == 1:
                st.info(first_try)
            st.info(f"Error correction {current_try}/{CODE_CORRECTION_TRIES} running...")
            corrected = extract_message(call_model(CODE_CORRECTOR_MODEL, formatted, code_corrector_sys_prompt))
        current_try += 1
    return corrected

def code_refiner(code_snippet: str, extra_context: str):
    """
    Refines the code snippet using the GPT-3 model for code correction.
    
    Args:
        code_snippet (str): The code snippet to refine.
        extra_context (str): Additional context to provide to the model.
    
    Returns:
        str: The refined code snippet.
    """
    whole_prompt = f"Original code: {code_snippet}\n' User request: {extra_context}"
    refined_code = call_model(CODE_REFINER_MODEL, whole_prompt, code_refiner_sys_prompt)
    with open('data/prompt_history.log', 'a') as f:
        f.write(f"User request: {extra_context}\nUsing model: {CODE_REFINER_MODEL}\n")
    return refined_code
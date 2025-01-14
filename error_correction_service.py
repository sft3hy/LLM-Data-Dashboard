from fastapi import FastAPI
from pydantic import BaseModel
import io
import contextlib
from config import CODE_CORRECTION_TRIES
from utils.code_editor import correct_code
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend



app = FastAPI()

class CodeSnippet(BaseModel):
    code: str
    extra_context: str
    file_name: str

@app.post("/correct_code/")
def correct_code_endpoint(code_snippet: CodeSnippet):
    current_try = 1
    corrected = code_snippet.code
    first_try_message = "The generated code was good but not perfect. Correcting errors now."

    while current_try <= CODE_CORRECTION_TRIES:
        try:
            # Attempt to execute the code
            exec_environment = {}
            with contextlib.redirect_stdout(io.StringIO()):
                exec(corrected, exec_environment)
            return {"status": "success", "corrected_code": corrected}
        except Exception as e:
            # Prepare correction context
            formatted = (
                f"This is the code: {corrected}\n"
                f"This is the error: {e}\n"
                f"This is the context: {code_snippet.extra_context}\n"
                f"Please output the corrected code"
            )
            corrected = correct_code(code_snippet=code_snippet.code, extra_context=code_snippet.extra_context, file_name=code_snippet.file_name)

            if current_try == CODE_CORRECTION_TRIES:
                return {"status": "error", "error_message": str(e), "corrected_code": corrected}
        current_try += 1

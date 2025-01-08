import os
import json
from datetime import datetime
from config import STORAGE_FILE, get_now

# File to store messages (can be replaced with a database)



def load_messages():
    """Load messages from storage."""
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_messages(messages):
    """Save messages to storage."""
    with open(STORAGE_FILE, "w") as f:  # Use 'w' to overwrite the file with updated content
        json.dump(messages, f, indent=4)

def get_file_messages(file_path):
    """Retrieve messages for a specific file."""
    messages = load_messages()
    return messages.get(file_path, [])

def set_file_messages(file_path, file_messages):
    """Store messages for a specific file."""
    messages = load_messages()
    messages[file_path] = file_messages
    save_messages(messages)

def add_user_message(file_path, message_contents, user_id):
    messages = load_messages()
    if file_path not in messages:
        messages[file_path] = []
    messages[file_path].append({
            "role": "user",
            "message_contents": message_contents,
            "timestamp": get_now(),
            "user_id": user_id,
        })
    save_messages(messages)


def add_assistant_message(file_path, message_contents, assistant_code_expander, assistant_code, assistant_code_top):
    """Add a message to a specific file."""
    messages = load_messages()
    if file_path not in messages:
        messages[file_path] = []
    messages[file_path].append({
        "role": "assistant",
        "message_contents": message_contents,
        "assistant_code": assistant_code,
        "assistant_code_expander": assistant_code_expander,
        "assistant_code_top": assistant_code_top,
        "timestamp": get_now()
    })
    save_messages(messages)


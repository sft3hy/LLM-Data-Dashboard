import json
import time
import schedule

# Models with initial counts
data = {
    "GROQ_MODELS": {
        "llama-3.3-70b-versatile": 0,
        "llama-3.3-70b-versatile": 0,
        "llama-3.1-70b-versatile": 0,
        "llama3-70b-8192": 0,
        "gemma2-9b-it": 0,
        "mixtral-8x7b-32768": 0,
    },
    "GOOGLE_MODELS": {"gemini-2.0-flash-exp": 0, "gemini-1.5-flash": 0},
    "OPENAI_MODELS": {"gpt-4o": 0, "gpt-4o-mini": 0},
}

FILE_PATH = "data/model_counts.json"


# Save the initial JSON structure to a file
# with open(FILE_PATH, "w") as file:
#     json.dump(data, file, indent=4)


# Function to update the count
def update_model_count(model_name, increment=True):
    try:
        # Load the JSON data
        with open(FILE_PATH, "r") as file:
            data = json.load(file)

        # Find and update the model count
        for model, count in data.items():  # Unpack each item as model, count
            if model == model_name:
                if increment:
                    data[model] += 1
                else:
                    data[model] = max(0, data[model] - 1)  # Prevent negative counts
                break
        else:
            raise ValueError(f"Model '{model_name}' not found.")

        # Save the updated data back to the file
        with open(FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)

        print(f"Updated {model_name}: {data[model_name]}")
    except Exception as e:
        print(f"Error: {e}")


# Function to reset counts to 0
def reset_counts():
    try:
        # Write the initial structure back to the file
        with open(FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)
        print("Counts reset to 0 at midnight.")
    except Exception as e:
        print(f"Error resetting counts: {e}")


# Schedule the reset task
schedule.every().day.at("00:00").do(reset_counts)


# Function to continuously check the schedule
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

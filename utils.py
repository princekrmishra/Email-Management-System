import json

def load_config(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Configuration file '{file_path}' not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Configuration file '{file_path}' is not a valid JSON.")
        return {}

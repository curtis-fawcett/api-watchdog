import json
import os

settings_file = "settings.json"
slow_response_threshold = 500

def set_slow_response_threshold(new_threshold):
    global slow_response_threshold

    slow_response_threshold = new_threshold

    settings ={"slow_response_threshold": new_threshold}

    with open(settings_file, "w") as file:
        json.dump(settings, file)

def load_settings():
    global slow_response_threshold

    if not os.path.exists(settings_file):
        return

    with open(settings_file, "r") as file:
        settings = json.load(file)
        saved_threshold = settings["slow_response_threshold"]
        slow_response_threshold = saved_threshold
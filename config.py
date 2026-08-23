import json
import os

settings_file = "settings.json"
DEFAULT_SLOW_RESPONSE_THRESHOLD = 500
slow_response_threshold = DEFAULT_SLOW_RESPONSE_THRESHOLD

def set_slow_response_threshold(new_threshold):
    global slow_response_threshold

    slow_response_threshold = new_threshold

    settings = {"slow_response_threshold": new_threshold}

    with open(settings_file, "w") as file:
        json.dump(settings, file)

def load_settings():
    global slow_response_threshold

    if not os.path.exists(settings_file):
        slow_response_threshold = DEFAULT_SLOW_RESPONSE_THRESHOLD
        return
    try:
        with open(settings_file, "r") as file:
            settings = json.load(file)
            saved_threshold = settings["slow_response_threshold"]
            if isinstance(saved_threshold, int) and saved_threshold > 0:
                slow_response_threshold = saved_threshold
            else:
                slow_response_threshold = DEFAULT_SLOW_RESPONSE_THRESHOLD
                print("Warning: Invalid slow response threshold. Using default setting.")

    except json.JSONDecodeError:
        slow_response_threshold = DEFAULT_SLOW_RESPONSE_THRESHOLD
        print("Warning: Could not load settings. Using default settings.")
    except KeyError:
        slow_response_threshold = DEFAULT_SLOW_RESPONSE_THRESHOLD
        print("Warning: Slow response threshold missing. Using default setting.")
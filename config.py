import json
import os


SETTINGS_FILE = "settings.json"
DEFAULT_SLOW_RESPONSE_THRESHOLD = 500
slow_response_threshold = DEFAULT_SLOW_RESPONSE_THRESHOLD


def set_slow_response_threshold(new_threshold):
    """Update and save the slow response threshold."""
    global slow_response_threshold

    slow_response_threshold = new_threshold

    settings = {
        "slow_response_threshold": new_threshold
    }

    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def load_settings():
    """Load the saved slow response threshold."""
    global slow_response_threshold

    if not os.path.exists(SETTINGS_FILE):
        slow_response_threshold = DEFAULT_SLOW_RESPONSE_THRESHOLD
        return

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)

        saved_threshold = settings.get("slow_response_threshold")

        if isinstance(saved_threshold, int) and saved_threshold > 0:
            slow_response_threshold = saved_threshold
            return

        slow_response_threshold = DEFAULT_SLOW_RESPONSE_THRESHOLD
        print(
            "Warning: Invalid slow response threshold. "
            "Using default setting."
        )

    except json.JSONDecodeError:
        slow_response_threshold = DEFAULT_SLOW_RESPONSE_THRESHOLD
        print("Warning: Could not load settings. Using default settings.")
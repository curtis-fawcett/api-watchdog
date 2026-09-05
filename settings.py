import config

def show_settings():
    print("Settings")
    print()

    print("Current slow response threshold:", config.slow_response_threshold, "ms")
    settings_choice = input("Enter new threshold in ms: ")

    if settings_choice == "":
        print("Threshold cannot be empty")
    else:
        try:
            new_threshold = int(settings_choice)

            if new_threshold <= 0:
                print("Threshold must be greater than 0")
            else:
                config.set_slow_response_threshold(new_threshold)
                print("Slow response threshold updated to", new_threshold, "ms")
        except ValueError:
            print("Threshold must be a whole number")
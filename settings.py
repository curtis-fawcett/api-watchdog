import config


def show_current_threshold():
    """Display the current slow response threshold."""
    print()
    print(
        "Current slow response threshold:",
        config.slow_response_threshold,
        "ms"
    )


def change_threshold():
    """Get and save a new slow response threshold."""
    while True:
        threshold_input = input(
            "Enter new threshold in ms (or 0 to go back): "
        ).strip()

        if threshold_input == "0":
            return

        if not threshold_input:
            print("Threshold cannot be empty.")
            continue

        try:
            new_threshold = int(threshold_input)

            if new_threshold <= 0:
                print("Threshold must be greater than 0.")
                continue

            config.set_slow_response_threshold(new_threshold)
            print(
                "Slow response threshold updated to",
                new_threshold,
                "ms"
            )
            return

        except ValueError:
            print("Threshold must be a whole number.")


def show_settings():
    """Display and update the slow response threshold."""
    while True:
        print("Settings")
        print()
        print("1. View current threshold")
        print("2. Change threshold")
        print("3. Back")

        settings_choice = input("Choose an option: ").strip()

        if settings_choice == "1":
            show_current_threshold()

        elif settings_choice == "2":
            change_threshold()

        elif settings_choice == "3":
            return

        else:
            print("Invalid option.")
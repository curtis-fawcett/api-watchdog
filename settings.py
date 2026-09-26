import config


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
            print()
            print(
                "Current slow response threshold:",
                config.slow_response_threshold,
                "ms"
            )

        elif settings_choice == "2":
            settings_choice = input("Enter new threshold in ms (or 0 to go back): ").strip()

            if settings_choice == "0":
                continue

            if not settings_choice:
                print("Threshold cannot be empty.")
                continue

            try:
                new_threshold = int(settings_choice)

                if new_threshold <= 0:
                    print("Threshold must be greater than 0.")
                    continue

                config.set_slow_response_threshold(new_threshold)
                print(
                    "Slow response threshold updated to",
                    new_threshold,
                    "ms"
                )

            except ValueError:
                print("Threshold must be a whole number.")

        elif settings_choice == "3":
            return

        else:
            print("Invalid option.")
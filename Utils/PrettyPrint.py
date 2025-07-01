def print_path(time, path):
    print("\n")
    print("\n")

    print(f"\nTime Estimated : {time} minutes.")
    print("Decisions :")
    print("*" * 50)  # Separator for clarity
    for i, step in enumerate(path, start=1):
        print(f"Decision {i}: {step}")
    print("*" * 50)

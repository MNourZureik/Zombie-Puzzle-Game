from BFSSolver.Facts.Log import Log


def print_path(time, path):
    print(f"Time Estimated : {time} minutes.")
    print("Decisions :")
    print("*")  # Separator for clarity
    for i, step in enumerate(path, start=1):
        print(f"Decision {i}: {step}")
    print("*")


def print_search_tree(facts):
    print("\n--- BFS Search Tree by Level ---")

    levels = {}
    for fact in facts.values():
        if isinstance(fact, Log):
            level = fact["level"]
            if level not in levels:
                levels[level] = []
            levels[level].append(fact)

    # Sort levels by level number
    sorted_levels = sorted(levels.keys())

    # Print nodes for each level
    for level in sorted_levels:
        print(f"\n--- Level {level} ---")
        if not levels[level]:
            print("  (No nodes at this level)")
            continue

        for i, fact in enumerate(levels[level]):
            # Visual cues for the list
            connector = "└── " if i == len(levels[level]) - 1 else "├── "

            # State information
            state_info = f"Left: {list(fact['left'])}, Right: {list(fact['right'])}, Light: {fact['light']}, Time: {fact['time']}"

            # Action that led to this state
            move_info = ""
            if fact["path"]:
                move_info = f"Action: {fact['path'][-1]}"
            else:
                move_info = "Action: Initial State"

            print(f"{connector}{state_info} - {move_info}")

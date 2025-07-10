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
            level = fact.get("level", -1)
            if level not in levels:
                levels[level] = []
            levels[level].append(fact)

    sorted_levels = sorted(levels.keys())

    for level in sorted_levels:
        print(f"\n┌─── Level {level} ────────{"─" * (80 - 15)}┐")
        
        if not levels[level]:
            print("│  (No nodes at this level)                                                               │")
            print(f"└{"─" * 80}┘")
            continue

        for i, fact in enumerate(levels[level]):
            state_info = f"Left: {list(fact['left'])}, Right: {list(fact['right'])}, Light: {fact['light']}, Time: {fact['time']}"
            move_info = f"Action: {fact['path'][-1]}" if fact["path"] else "Action: Initial State"
            
            # Padding for alignment
            state_info_padded = state_info.ljust(60)
            move_info_padded = move_info.ljust(38)

            if i == 0:
                print(f"│ ┌─ Node {i+1} ─┐")
            else:
                print(f"│ ├─ Node {i+1} ─┤")

            print(f"│ │ State: {state_info_padded} │")
            print(f"│ │ Move:  {move_info_padded} │")

            if i == len(levels[level]) - 1:
                print(f"│ └────────┘")

        print(f"└{"─" * 80}┘")

from ForwardChaining.Facts.TimeExceeded import TimeExceeded


def print_path(time, path):
    print(f"\nTime Estimated : {time} minutes.")
    print("Decisions :")
    print("*")  
    for i, step in enumerate(path, start=1):
        print(f"Decision {i}: {step}")
    print("*")


def print_search_tree(facts):
    print("\n--- Search Tree ---")
    nodes = {}
    time_exceeded_facts = []
    for fact in facts.values():
        if "state_hash" in fact:
            nodes[fact["state_hash"]] = {"fact": fact, "children": []}
        elif isinstance(fact, TimeExceeded):
            time_exceeded_facts.append(fact)

    for fact in facts.values():
        if "parent_hash" in fact and fact["parent_hash"] in nodes:
            nodes[fact["parent_hash"]]["children"].append(nodes[fact["state_hash"]])

    def print_node(node, indent="", is_last=True):
        fact = node["fact"]

        connector = "└── " if is_last else "├── "

        level_info = f"Level {fact['level']}"
        state_info = f"Left: {list(fact['left'])}, Right: {list(fact['right'])}, Light: {fact['light']}, Time: {fact['time']}"

        move_info = ""
        if fact["path"]:
            move_info = f"Action: {fact['path'][-1]}"

        print(f"{indent}{connector}{level_info} - {state_info} - {move_info}")

        child_indent = indent + ("    " if is_last else "│   ")

        for i, child in enumerate(node["children"]):
            print_node(child, child_indent, i == len(node["children"]) - 1)

    for node in nodes.values():
        if node["fact"]["parent_hash"] is None:
            print_node(node)
            break

    if time_exceeded_facts:
        print("\n--- Time Exceeded States ---")
        for fact in time_exceeded_facts:
            print(
                f"Level {fact['level']}: Left: {list(fact['left'])}, Right: {list(fact['right'])}, Light: {fact['light']}, Time: {fact['time']} - Path leads to time exceeded"
            )

from DFSSolver.Facts.Log import Log


def print_path(time, path):
    """Prints the final solution path in a readable format."""
    print(f"--- Solution Path ---")
    print(f"Total Time: {time} minutes.")
    print("Steps:")
    for i, step in enumerate(path, start=1):
        print(f"  {i}. {step}")
    print("-" * 25)


def pretty_search_tree(facts):
    """Prints the entire DFS search tree in a structured and readable format."""
    print("--- DFS Search Tree ---")

    logs = sorted(
        [fact for fact in facts.values() if isinstance(fact, Log)],
        key=lambda x: x.get('time', 0)
    )

    if not logs:
        print("  (No search history available)")
        return

    nodes = {fact["state_hash"]: fact for fact in logs}
    children_map = {hash_val: [] for hash_val in nodes}
    root_node = None

    for log in logs:
        parent_hash = log.get("parent_hash")
        if parent_hash in nodes:
            children_map[parent_hash].append(log)
        elif not parent_hash:
            root_node = log

    def print_tree_recursive(node, prefix="", is_last=True):
        """Recursively prints the tree structure."""
        state_hash = node["state_hash"]
        
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{_format_node(node)}")

        child_prefix = prefix + ("    " if is_last else "│   ")
        node_children = children_map.get(state_hash, [])
        for i, child in enumerate(node_children):
            print_tree_recursive(child, child_prefix, i == len(node_children) - 1)

    if root_node:
        print_tree_recursive(root_node)
    else:
        print("  (Could not determine the root of the search tree)")


def _format_node(node):
    """Formats a single node for printing."""
    left = ", ".join(sorted(node['left']))
    right = ", ".join(sorted(node['right']))
    time = node['time']
    move = node['path'][-1] if node['path'] else "Initial State"
    
    return f"[{time}m] L:{{{left}}} R:{{{right}}} | Action: {move}"


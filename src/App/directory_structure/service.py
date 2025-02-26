from collections import defaultdict

def print_tree(tree: dict, prefix: str = "", is_last: bool = True, max_items: int = 30) -> str:
    """Recursively prints a tree-like dictionary structure with properly aligned vertical lines."""
    output = []
    items = list(tree.items())[:max_items]
    total_items = len(tree)

    for i, (key, sub_tree) in enumerate(items):
        is_last_item = (i == len(items) - 1)
        branch = "└── " if is_last_item else "├── "
        new_prefix = prefix + ("    " if is_last_item else "│   ")  # Maintain vertical lines

        output.append(f"\n{prefix}{branch}{key}")

        if isinstance(sub_tree, dict) and sub_tree:
            output.append(print_tree(sub_tree, new_prefix, is_last_item, max_items))

    if total_items > max_items:
        output.append(f"{prefix}└── ...")  # Indicating more items exist

    return "".join(output)


def build_tree(paths):
        tree = defaultdict(dict)
        for file in paths:
            path = file  # Extract filename from file object
            parts = path.split("/")                        
            node = tree
            for part in parts:
                node = node.setdefault(part, {}) 
        return tree
      
def get_directory_structure(files):
    filtered_files = []
    for file in files:
        full_path = file
        # start with
        paths = full_path.split("/")
        checkFile = True
        for path in paths:        
            exclusions = [            # Files that start with a dot
                "__pycache__",        # Python bytecode cache folder
                ".git",               # Git directory
                ".svn",               # Subversion directory
                ".idea",              # IDE project folder (e.g., PyCharm)
                "node_modules",       # Node.js modules directory
                "dist",               # Build directory for many languages
                "build",              # Build directory
                ".vscode",            # Visual Studio Code settings
                ".DS_Store",          # macOS-specific file
                "README.md",          # README file
                ]
            if any(exclusion in path for exclusion in exclusions) or path.startswith("."):
                checkFile = False
        if checkFile:
            filtered_files.append(file)
    
    directory_tree = build_tree(filtered_files)
    return print_tree(directory_tree)

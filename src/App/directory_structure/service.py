from collections import defaultdict

def get_directory_structure(files):
    def build_tree(paths):
        content_files = ""
        tree = defaultdict(dict)
        for file in paths:
            path = file.filename  # Extract filename from file object
            parts = path.split("/")                        
            node = tree
            for part in parts:
                node = node.setdefault(part, {})
            try:                
                binary_content = file.read()
                content = binary_content.decode('utf-8')  
                content_files += f"\n{path}\n<pre><code>{content}</code></pre>\n"  # Append the file name and content  # Now it correctly modifies the outer variable
            except UnicodeDecodeError:
                continue 
        return tree, content_files
    
    def print_tree(node, indent=""):
        result = ""
        for key, subnode in sorted(node.items()):
            result += f"{indent}{key}\n"
            result += print_tree(subnode, indent + "    ")
        return result
    
    directory_tree, contents = build_tree(files)
    return print_tree(directory_tree), contents

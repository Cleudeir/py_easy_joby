import os

def get_directory_structure(directory_path):
    if not os.path.exists(directory_path):
        return "Directory does not exist."

    structure = []
    for dirpath, dirnames, filenames in os.walk(directory_path):
        # Ignore any directories that start with '.' or '__'
        dirnames[:] = [d for d in dirnames if not (d.startswith('.') or d.startswith('__'))]

        # Calculate the level of indentation
        level = dirpath.replace(directory_path, '').count(os.sep)
        indent = ' ' * 4 * level
        structure.append(f"{indent}{os.path.basename(dirpath)}/")
        
        # Add files, ignoring those that start with '.' or '__'
        subindent = ' ' * 4 * (level + 1)
        for f in filenames:
            if not (f.startswith('.') or f.startswith('__')):
                structure.append(f"{subindent}{f}")

    return "\n".join(structure)

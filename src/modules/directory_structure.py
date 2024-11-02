import os

def get_directory_structure(directory_path):
    if not os.path.exists(directory_path):
        return "Directory does not exist."

    structure = []
    for dirpath, dirnames, filenames in os.walk(directory_path):
        # Ignore any directories that start with a dot
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]  # Update dirnames in-place

        level = dirpath.replace(directory_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        structure.append(f"{indent}{os.path.basename(dirpath)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in filenames:
            structure.append(f"{subindent}{f}")

    return "\n".join(structure)

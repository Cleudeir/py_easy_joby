import os
import uuid


def get_concatenate_project(directory_path):
    if not os.path.exists(directory_path):
        return "Directory does not exist."

    # Generate a unique file name for the concatenated file
    unique_file_name = f"concatenated_{uuid.uuid4().hex}.txt"
    unique_file_path = os.path.join(directory_path, unique_file_name)

    structure = []
    concatenated_content = []

    for dirpath, dirnames, filenames in os.walk(directory_path):
        # Ignore any directories that start with '.' or '__'
        dirnames[:] = [
            d for d in dirnames if not (d.startswith(".") or d.startswith("__"))
        ]

        # Calculate the level of indentation
        level = dirpath.replace(directory_path, "").count(os.sep)
        indent = " " * 4 * level
        structure.append(f"{indent}{os.path.basename(dirpath)}/")

        # Add files, ignoring those that start with '.' or '__'
        subindent = " " * 4 * (level + 1)
        for f in filenames:
            if not (f.startswith(".") or f.startswith("__")):
                structure.append(f"{subindent}{f}")

                # Read file content and append it to concatenated_content
                file_path = os.path.join(dirpath, f)
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        concatenated_content.append(f"--- Start of {f} ---\n")
                        concatenated_content.append(file.read())
                        concatenated_content.append(f"\n--- End of {f} ---\n")
                except Exception as e:
                    concatenated_content.append(f"\n--- Failed to read {f}: {e} ---\n")

    # Write the concatenated content into the unique file
    try:
        with open(unique_file_path, "w", encoding="utf-8") as unique_file:
            unique_file.write("\n".join(concatenated_content))
    except Exception as e:
        return f"Failed to write concatenated file: {e}"

    # Read back the content of the unique file
    try:
        with open(unique_file_path, "r", encoding="utf-8") as unique_file:
            unique_file_content = unique_file.read()
    except Exception as e:
        return f"Failed to read concatenated file: {e}"

    # Return the directory structure and the unique file content
    return f"Directory structure:\n\n{chr(10).join(structure)}\n\nContent of the concatenated file:\n\n{unique_file_content}"

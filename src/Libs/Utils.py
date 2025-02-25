import time
import re

def normalize_path_name(path):
    return path.replace(" ", "_").replace(".", "_")

def parseTextToWeb(text):
    text_replace = text
    if("<" in text_replace):
            return text_replace.replace('<', '&lt;')
    return text_replace

def extract_code_blocks(text_replace):
    try:
        text_replace = text_replace
        if("```" in text_replace):
            pattern = r"```(?:\w+)?\n([\s\S]*?)```"
            matches = re.findall(pattern, text_replace)
            text_replace = [match.strip() for match in matches][0]
        return text_replace
    except Exception as e:
        print(f"Error extracting code blocks: {e}")
        return text_replace

def extract_code_replace(text):
    try:
        pattern = r"```(?:\w+)?\n([\s\S]*?)```"
        matches = re.findall(pattern, text)
        return [match.strip() for match in matches][0]
    except Exception as e:
        print(f"Error extracting code blocks: {e}")
        return ""
    
def time_format_string(start_time):
    response_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    if response_time < 1000:
        return f"{response_time:.0f} ms"

    seconds = response_time / 1000
    if seconds < 60:
        return f"{seconds:.2f} s"

    minutes = seconds / 60
    if minutes < 60:
        return f"{int(minutes)} min {seconds % 60:.2f} s"

    hours = minutes / 60
    if hours < 24:
        return f"{int(hours)} h {int(minutes % 60)} min {seconds % 60:.2f} s"

    days = hours / 24
    if days < 30:
        return f"{int(days)} d {int(hours % 24)} h {int(minutes % 60)} min {seconds % 60:.2f} s"

    months = days / 30
    return f"{int(months)} m {int(days % 30)} d {int(hours % 24)} h {int(minutes % 60)} min {seconds % 60:.2f} s"


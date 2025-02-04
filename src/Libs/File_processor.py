import re
import pdfplumber
import docx
from src.Libs.Files import save_content_to_file
from src.Libs.LLM.Provider import get_text
from src.Libs.Utils import extract_code_blocks

def split_file_by_text(file_content, split_text, uploads_dir):
    """
    Split the given file content by the provided text.
    :param file_content: The content of the file as a string
    :param split_text: The text to use as the splitting point
    :return: A list of strings, each representing a section of the split content
    """
    sections = file_content.split(split_text)
    insertSplit_text = []
    for index in range(len(sections)):
        section = sections[index]
        content = f"{split_text} {section}"
        save_content_to_file(f"{uploads_dir}{index}.txt", content)
        insertSplit_text.append(content)
        
    return insertSplit_text

def split_file_by_regex(file_content, regex, uploads_dir):
    print("regex", regex)
    """
    Split the given file content by the provided text.
    :param file_content: The content of the file as a string
    :param split_text: The text to use as the splitting point
    :return: A list of strings, each representing a section of the split content
    """

    sections = re.findall(regex, file_content, re.DOTALL)
    insertSplit_text = []
    for index in range(len(sections)):
        section = sections[index]
        user_prompt = f"""{section} make refactoring this code remove 'this', and add comments step by step, rewrite complete code , follow structure:
```javascript
code 
```
        """
        refactoring  = extract_code_blocks(get_text("You are a software engineer. will create documentation", user_prompt))
        user_prompt= f"""
this is a code, you need summary:
{section}
Create a once-paragraph summary using layman's terms and non-technical. no use of code, creation of summary, no comments, no suggestions, no corrections, no explanation.
Follow this structure markdown:  
    ...(once-paragraph)
"""
        summary = get_text("You are a software engineer. will create documentation", user_prompt )
        save_content_to_file(f"{uploads_dir}{index}.md", f"""
## Original function

    {section}
    
## refectory code

    {refactoring }
    
## Summary

    {summary}
""")
        insertSplit_text.append(refactoring )
        
    return insertSplit_text

def split_file_by_lines(file_content, lines_per_section):
    """
    Split the file content into sections based on the number of lines.
    :param file_content: The content of the file as a string
    :param lines_per_section: Number of lines per section
    :return: A list of strings, each representing a section of the split content
    """
    lines = file_content.splitlines()
    sections = [lines[i:i+lines_per_section] for i in range(0, len(lines), lines_per_section)]
    return ['\n'.join(section) for section in sections]

def split_file_by_paragraphs(file_content):
    """
    Split the file content into sections based on paragraphs.
    :param file_content: The content of the file as a string
    :return: A list of paragraphs
    """
    paragraphs = file_content.split('\n')
    return paragraphs

def read_pdf(file):
    """
    Extract text from a PDF file while preserving original formatting.
    :param file: File object (PDF)
    :return: The text content of the PDF as a string
    """
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            # Extract text from the page, preserving layout
            text += page.extract_text() + "\n"
    return text

def read_docx(file):
    """
    Extract text from a DOCX file.
    :param file: File object (DOCX)
    :return: The text content of the DOCX as a string
    """
    doc = docx.Document(file)
    return '\n'.join([para.text for para in doc.paragraphs])

def read_txt(file):
    """
    Extract text from a TXT file.
    :param file: File object (TXT)
    :return: The text content of the TXT as a string
    """
    return file.read().decode('utf-8')

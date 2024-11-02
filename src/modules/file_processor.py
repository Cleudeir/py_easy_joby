import pdfplumber
import docx

def split_file_by_text(file_content, split_text):
    """
    Split the given file content by the provided text.
    :param file_content: The content of the file as a string
    :param split_text: The text to use as the splitting point
    :return: A list of strings, each representing a section of the split content
    """
    sections = file_content.split(split_text)
    return sections

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
    paragraphs = file_content.split('\n\n')
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

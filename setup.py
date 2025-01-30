from setuptools import setup, find_packages

setup(
    name="Easy_Job",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "flask",
        "flasgger",
        "pdfplumber",
        "python-docx",
        "ollama",
        "markdown",
        "google-generativeai",
        "python-dotenv",
        "scikit-learn",
        "jinja2",
        "pypandoc",
        "pytesseract",
        "pillow",
    ],
)

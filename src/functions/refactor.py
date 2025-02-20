from src.Libs.LLM.Provider import (
    get_ollama_embeddings,
    get_ollama_text,
    get_genai_text,
)
from sklearn.metrics.pairwise import cosine_similarity


def get_agent_separate(gpt_provider,  file_content):
    system_prompt = "You are a software engineer"
    user_prompt = f"""
    {file_content}
    refactor this code, separate in functions, only create code, no comments in code, no explanation, only code. create with perfect indentation, create complete code.
    """
    # Use Ollama to generate the summary with the specified model
    if gpt_provider == "ollama":
        data = get_ollama_text(system_prompt, user_prompt)
    elif gpt_provider == "gemini":
        data = get_genai_text(system_prompt, user_prompt)
    # Check if the response is a dictionary, which indicates an error
    if isinstance(data, dict) and "error" in data:
        return f"**Error**: {data['error']}\n"
    # Return the formatted summary
    return data


def get_agent_similarity(file_content, reconstruct_code):
    embeddings_code = get_ollama_embeddings(        text_input=file_content
    )
    embeddings_reconstruct_code = get_ollama_embeddings(        text_input=reconstruct_code
    )
    similarity = cosine_similarity(embeddings_code, embeddings_reconstruct_code)
    return similarity[0][0]

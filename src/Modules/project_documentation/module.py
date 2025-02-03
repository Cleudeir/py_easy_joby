from src.Libs.LLM.Provider import get_text



def get_summary(content):
    system_prompt = """
    you are a software engineer create documentation explain to the user.  
    """ 
    # ----------------------------------------------------------------------
    user_prompt = f"""
    This is a file, you need summary:
    {content}
    Create this one-paragraph summary using layman's terms and non-technical. no use of code, creation of summary, no comments, no suggestions, no corrections, no explanation.
    Follow this structure markdown:  
    ## Summary
        ...(once paragraph)
    """
    summary = get_text(system_prompt, user_prompt)   
    return summary

def get_generate_code(file_name, summary):
    system_prompt = """
    you are a software engineer.  
    """ 
    # ----------------------------------------------------------------------
    user_prompt = f"""
    That is summary the code:
    {summary}
    create code for file:{file_name}
        -use best practices, 
        -complete with all function and logics
        -no use of code
        -no comments
        -no explanation.
        -using perfect indentation     
    """
    code = get_text(system_prompt, user_prompt)
    # ----------------------------------------------------------------------   
    return code

def get_final_summary(summary):
    system_prompt = """
    you are a software engineer create documentation explain to the user. use all time to elaborate best summary.
    """
    # ----------------------------------------------------------------------
    user_prompt = f"""  
    That is summary:
    {summary}
    Create a three-paragraph summary using this summary code files, create a summary explain this code base works, your business rules. no use code, no comments, no explanation.
    Follow this structure to create a summary:
    ## Summary
        ...(in details)
    ## Business Rules
        ...(bullet points)   
    ## Tech Stack 
        ...(bullet points)
    """
    _summary = get_text(system_prompt, user_prompt)
    # ----------------------------------------------------------------------   
    return _summary
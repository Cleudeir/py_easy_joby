from src.Libs.LLM.Provider import get_text



def get_summary(content):
    system_prompt = """
    you are a software engineer create documentation explain to the user.  
    """ 
    # ----------------------------------------------------------------------
    user_prompt = f"""
    This is a file, you need summary:
    {content}
    Create this one-paragraph summary using terms as an explainer for 18 year olds. no use of code, creation of summary, no comments, no suggestions, no corrections, no explanation.
    Follow this structure markdown:  
    ## Summary
        ...(once paragraph)
    """
    summary = get_text(system_prompt, user_prompt)   
    return summary

def get_summary_fix_follow(content, filename):
    system_prompt = """
    you are a software engineer create documentation explain to the user.  
    """ 
    # ----------------------------------------------------------------------
    user_prompt = f"""
    This is a summary created :
    {content}
    This is a structure:
       ----
        ## File name
        - {filename}
        ##  Project purpose and description
            ... 
        ----
    check this summary flow structure, and fix if exists errors:
     - If exists code , remove all code if exists code, create summary without code.
     - If exists commends, remove all commends.
     - If exists explanations, remove all explanations.
     - If exists suggestions, remove all suggestions.
    """
    summary = get_text(system_prompt, user_prompt)   
    return summary

def get_final_summary(summary):
    system_prompt = """
    you are a software engineer create documentation explain to the user.
    """
    # ----------------------------------------------------------------------
    user_prompt = f"""  
    That is summary:
    {summary}
    Follow this structure to create a summary:
    ## Summary
        ...(in details) 
    ## Tech Stack 
        ...(bullet points)
    obs: Create summary using terms like a explainer to children 18 years old. no use code, Create summary, no comments, no suggestions any fix, no explanation.
    """
    _summary = get_text(system_prompt, user_prompt)
    # ----------------------------------------------------------------------   
    return _summary
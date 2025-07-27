import os
from dotenv import load_dotenv

load_dotenv()

workday_email = os.getenv("WORKDAY_EMAIL")
workday_pass = os.getenv("WORKDAY_PASS")

def get_prompt(resume_text: str) -> str:
    """
    Generate the prompt for the Playwright agent based on the resume text.
    
    Args:
        resume_text (str): The text extracted from the resume PDF.
        
    Returns:
        str: The formatted prompt string.
    """
    if not workday_email or not workday_pass:
        raise ValueError("Environment variables WORKDAY_EMAIL and WORKDAY_PASS must be set")
    prompt = f'''

    go to google.com search for nvidia jobs.
    Go to workday jobs page.
    go to wd5.myworkdayjobs only after searching
    
    login with my email: {workday_email} with password: {workday_pass}.
    
    search for a job based on the resume details use broad search, don't make it too specific.

    pickup any job that matches the resume details and apply for it.

    Use apply manually option and fill the details manually based on the resume details.
    Fill each field one by one, don't fill all at once.
    
    Resume Details:
    <resume_text>
    {resume_text}
    </resume_text>
    '''
    return prompt.strip()
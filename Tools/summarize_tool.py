from langchain_core.tools import tool
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm=ChatGroq(model="llama-3.1-8b-instant",
             api_key=os.getenv('GROQ_API_KEY'))

@tool
def summarize_email(content:str)->str:
    """summerize the email in 3 bullit points"""
    if not content:
        return "no content to summarize"
    
    prompt=f" Summerize the emails in 3 bullit points :{content}"

    responce=llm.invoke(prompt)
    print(responce.content)
    return responce.content
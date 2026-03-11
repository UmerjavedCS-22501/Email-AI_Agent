from langchain_core.tools import tool
import requests
import os
from dotenv import load_dotenv

load_dotenv()
slack_webhock=os.getenv("SLACK_WEBHOOK")

@tool
def sent_to_slack(input:str):
    """Message sent to slack channel"""
    if not input:
        return "no message to sent "
    payload={'text':input}
    responce=requests.post(slack_webhock,json=payload)

    if responce.status_code==200:
        return "message sent on slack"
    else:
        return f"faild to sent message .status code {responce.status_code}"
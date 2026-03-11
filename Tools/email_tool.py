from langchain_core.tools import tool
from dotenv import load_dotenv
import os
import imaplib
import email
from email.header import decode_header

load_dotenv()


Email=os.getenv("Email")
Password=os.getenv("APP_PASSWORD")


@tool
def cheak_unread_email()->str:
    """Cheak unread email and sent their contant"""
    mail=imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(Email,Password)
    mail.select('inbox')

    status,message=mail.search(None,'UNSEEN')
    email_ids=message[0].split()

    if not email_ids:
        return "No unread email"
    emails = []

    for e_id in email_ids[:5]:  # Limit number of emails
        status, msg_data = mail.fetch(e_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        # Decode subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        # Get email body
        if msg.is_multipart():
            # Loop through parts and pick plain text
            body = next(
                (part.get_payload(decode=True).decode() 
                 for part in msg.walk() 
                 if part.get_content_type() == "text/plain"), 
                ""
            )
        else:
            body = msg.get_payload(decode=True).decode()

        emails.append(f"Subject: {subject}\nBody: {body}")

    return "\n\n".join(emails)
from Tools.email_tool import cheak_unread_email
from Tools.slack_tool import sent_to_slack
from Tools.summarize_tool import summarize_email


def chunk_emails(emails_text: str, chunk_size: int = 3):
    """Split emails string into chunks of `chunk_size` emails each."""
    emails_list = emails_text.strip().split("\n\n")
    for i in range(0, len(emails_list), chunk_size):
        yield "\n\n".join(emails_list[i:i + chunk_size])


class EmailAgent:
    def run(self):
        # 1️ Get unread emails
        emails = cheak_unread_email.invoke("")
        if emails == "No unread email":
            print("No unread emails found.")
            return

        # 2️ Split emails into chunks to avoid token errors
        for chunk in chunk_emails(emails, chunk_size=3):
            # 3️ Summarize each chunk
            summary = summarize_email.invoke(chunk)
            # 4️ Send summary to Slack
            sent_to_slack.invoke(summary)
            print("Chunk summarized and sent to Slack!")

        print("Agent Complete: emails summarized and sent to Slack!")
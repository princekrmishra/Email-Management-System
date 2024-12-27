import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email credentials from environment variables
EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

def connect_to_email_server():
    """
    Connect to the IMAP server and login.
    """
    try:
        server = imaplib.IMAP4_SSL("imap.gmail.com")
        server.login(EMAIL, PASSWORD)
        return server
    except Exception as e:
        print(f"Error connecting to the email server: {e}")
        return None

def fetch_emails(server, folder="INBOX", search_criteria="ALL"):
    """
    Fetch emails from a specified folder using a search criteria.
    """
    try:
        server.select(folder)
        status, messages = server.search(None, search_criteria)
        email_ids = messages[0].split()
        print(f"Found {len(email_ids)} emails.")

        for email_id in email_ids[-5:]:  # Fetch the last 5 emails
            status, msg_data = server.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    process_email(msg, email_id, server)
    except Exception as e:
        print(f"Error fetching emails: {e}")

def process_email(msg, email_id, server):
    """
    Process the email content and send a response.
    """
    # Decode the email subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else "utf-8")
    print(f"Subject: {subject}")

    # Decode email sender
    from_ = msg.get("From")
    sender_email = email.utils.parseaddr(from_)[1]
    print(f"From: {from_}")

    # Check the email body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode()
    else:
        body = msg.get_payload(decode=True).decode()
    print(f"Body:\n{body}")

    # Decide whether to respond
    if "specific keyword" in body.lower() or "specific subject" in subject.lower():
        send_response(sender_email, f"Re: {subject}", "Thank you for your email. Here is an automated response.")

def send_response(to_address, subject, body):
    """
    Send a response email.
    """
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL, PASSWORD)
            msg = MIMEMultipart()
            msg["From"] = EMAIL
            msg["To"] = to_address
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            server.sendmail(EMAIL, to_address, msg.as_string())
        print(f"Automated response sent to {to_address}.")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    """
    Main function to automate email retrieval and responses.
    """
    server = connect_to_email_server()
    if server:
        fetch_emails(server)
        server.logout()

if __name__ == "__main__":
    main()

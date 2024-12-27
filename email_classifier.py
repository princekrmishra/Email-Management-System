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

# Expanded classification logic with more keywords
def classify_email(subject, body, sender):
    # Personal email keywords
    personal_keywords = [
    "family", "friend", "party", "vacation", "birthday", "greetings", "love",
    "invitation", "photos", "memories", "holiday", "wedding", "thanks",
    "congratulations", "weekend", "care", "shopping", "hobby", "reunion",
    "chat", "meetup", "catch up", "thinking of you", "home", "get-together",
    "kids", "pets", "fun", "movies", "travel", "beach", "cooking", "dinner",
    "books", "hiking", "festivals", "anniversary", "good news", "relax",
    "plans", "event", "mom", "dad", "siblings", "daughter", "son", "cousins",
    "gathering", "picnic", "trip", "free time", "hangout", "bonding", "happiness",
    "funny", "laugh", "gift", "flowers", "cake", "reminder", "warm wishes",
    "thinking of you", "phone call", "celebration", "long time no see", 
    "updates", "personal", "catching up", "visiting", "sharing", "stories",
    "memories", "conversations", "emotions", "miss you", "care package",
    "fun time", "adventure", "road trip", "stay safe"
    ]

    # Professional email keywords
    professional_keywords = [
    "invoice", "meeting", "project", "proposal", "deadline", "report", "HR",
    "salary", "promotion", "team", "conference", "client", "interview",
    "feedback", "offer", "agenda", "official", "contract", "agreement",
    "recruitment", "resignation", "work", "follow-up", "task", "delivery",
    "business", "vendor", "update", "performance", "appraisal", "training",
    "presentation", "collaboration", "minutes of meeting", "status report",
    "scope", "timeline", "budget", "resource", "assignment", "productivity",
    "workflow", "strategy", "KPI", "review", "consultation", "performance review",
    "escalation", "risk management", "teamwork", "milestone", "announcement",
    "corporate", "policy", "procedures", "memo", "internal", "external",
    "partnership", "sales", "marketing", "operations", "engineering", "QA",
    "compliance", "logistics", "onboarding", "benchmark", "standards",
    "vision", "mission", "alignment", "execution", "business case", "RFP",
    "project plan", "weekly update", "quarterly report", "stakeholders"
    ]

    # Spam email keywords
    spam_keywords = [
    "free", "win", "offer", "click", "sale", "lottery", "guaranteed",
    "discount", "promotion", "act now", "limited time", "risk-free", "deal",
    "urgent", "gift", "congratulations", "exclusive", "100%", "cheap",
    "best price", "winner", "claim", "casino", "jackpot", "loan", "easy money",
    "make millions", "no risk", "sex", "adult", "porn", "viagra", "investment",
    "unsubscribe", "quick cash", "amazing deal", "instant results", "unlock",
    "bonus", "limited offer", "get rich", "hidden fees", "earn now",
    "buy now", "secret", "double your money", "trial", "upgrade",
    "exclusive content", "work from home", "fast money", "click here",
    "secure payment", "act immediately", "urgent notice", "credit card",
    "free trial", "win big", "free gift", "special rate", "hot deal",
    "membership", "miracle", "lose weight fast", "as seen on", "best deal",
    "urgent approval", "luxury", "exclusive opportunity", "watch now",
    "profit", "hidden offer", "zero cost", "lifetime access", "call now"
    ]


    # Combine all inputs for classification
    combined_text = f"{subject} {body} {sender}".lower()

    if any(keyword in combined_text for keyword in personal_keywords):
        return "Personal"
    elif any(keyword in combined_text for keyword in professional_keywords):
        return "Professional"
    elif any(keyword in combined_text for keyword in spam_keywords):
        return "Spam"
    else:
        return "Uncategorized"

def connect_to_email_server():
    """
    Connect to the IMAP server and login.
    """
    try:
        # Connect to the server
        server = imaplib.IMAP4_SSL("imap.gmail.com")
        server.login(EMAIL, PASSWORD)
        return server
    except Exception as e:
        print(f"Error connecting to the email server: {e}")
        return None

def fetch_recent_emails(server, folder="INBOX", count=15):
    """
    Fetch the 'count' most recent emails.
    """
    try:
        server.select(folder)  # Select the folder (e.g., INBOX)
        status, messages = server.search(None, "ALL")
        
        # Convert messages to a list of email IDs
        email_ids = messages[0].split()
        recent_email_ids = email_ids[-count:]  # Get the most recent 'count' emails
        print(f"Found {len(recent_email_ids)} recent emails.")
        
        for email_id in reversed(recent_email_ids):  # Fetch in reverse order (most recent first)
            status, msg_data = server.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    process_and_classify_email(msg)
    except Exception as e:
        print(f"Error fetching emails: {e}")

def process_and_classify_email(msg):
    """
    Process and classify the email content: decode headers, fetch body, and classify.
    """
    # Decode the email subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else "utf-8")

    # Decode email sender
    from_ = msg.get("From")

    # Process the email body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True).decode()
                break
    else:
        content_type = msg.get_content_type()
        if content_type == "text/plain":
            body = msg.get_payload(decode=True).decode()

    # Classify the email
    email_type = classify_email(subject, body, from_)
    
    # Display the email details and classification
    print("\n--- Email Received ---")
    print(f"Sender: {from_}")
    print(f"Subject: {subject}")
    print(f"Type: {email_type}")

def main():
    """
    Main function to fetch and classify recent emails.
    """
    server = connect_to_email_server()
    if server:
        fetch_recent_emails(server, count=15)  # Fetch only the 15 most recent emails
        server.logout()

if __name__ == "__main__":
    main()

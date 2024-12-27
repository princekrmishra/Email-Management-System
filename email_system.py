import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailManagementSystem:
    def __init__(self, records_file="email_records.json"):
        self.email_records_file = records_file
        self.load_email_records()

    def load_email_records(self):
        try:
            with open(self.email_records_file, "r") as file:
                self.email_records = json.load(file)
        except FileNotFoundError:
            self.email_records = []

    def save_email_records(self):
        with open(self.email_records_file, "w") as file:
            json.dump(self.email_records, file, indent=4)

    def send_email(self, sender_email, sender_password, recipient_email, subject, body, smtp_server, smtp_port):
        try:
            # Setup the email
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            # Send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)

            # Save the email record
            self.email_records.append({
                "sender": sender_email,
                "recipient": recipient_email,
                "subject": subject,
                "body": body
            })
            self.save_email_records()
            print("Email sent successfully!")

        except smtplib.SMTPException as e:
            print(f"Failed to send email: {e}")

    def view_emails(self):
        if not self.email_records:
            print("No emails sent yet.")
        else:
            for i, email in enumerate(self.email_records, start=1):
                print(f"Email {i}:")
                print(f"  Sender: {email['sender']}")
                print(f"  Recipient: {email['recipient']}")
                print(f"  Subject: {email['subject']}")
                print(f"  Body: {email['body']}\n")

    def search_emails(self, keyword):
        results = [
            email for email in self.email_records
            if keyword.lower() in email["recipient"].lower() or keyword.lower() in email["subject"].lower()
        ]
        if not results:
            print("No emails found matching the keyword.")
        else:
            for i, email in enumerate(results, start=1):
                print(f"Email {i}:")
                print(f"  Sender: {email['sender']}")
                print(f"  Recipient: {email['recipient']}")
                print(f"  Subject: {email['subject']}")
                print(f"  Body: {email['body']}\n")

    def delete_email(self, index):
        if 0 <= index < len(self.email_records):
            del self.email_records[index]
            self.save_email_records()
            print("Email record deleted successfully.")
        else:
            print("Invalid email index.")

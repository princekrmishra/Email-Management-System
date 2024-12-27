from email_system import EmailManagementSystem
from utils import load_config

def main():
    config = load_config("config.json")
    system = EmailManagementSystem()

    while True:
        print("\nEmail Management System")
        print("1. Send Email")
        print("2. View Sent Emails")
        print("3. Search Emails")
        print("4. Delete Email")
        print("5. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            sender = input("Enter your email: ")
            password = input("Enter your password: ")
            recipient = input("Enter recipient email: ")
            subject = input("Enter subject: ")
            body = input("Enter email body: ")
            system.send_email(
                sender,
                password,
                recipient,
                subject,
                body,
                smtp_server=config["smtp_server"],
                smtp_port=config["smtp_port"]
            )
        elif choice == "2":
            system.view_emails()
        elif choice == "3":
            keyword = input("Enter keyword to search: ")
            system.search_emails(keyword)
        elif choice == "4":
            system.view_emails()
            try:
                index = int(input("Enter the email index to delete (1-based): ")) - 1
                system.delete_email(index)
            except ValueError:
                print("Invalid input. Please enter a number.")
        elif choice == "5":
            print("Exiting Email Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    
    #fsvu wsks nnsy uvwy

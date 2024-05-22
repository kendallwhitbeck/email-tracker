"""
Program: email-tracker
Author: Kendall Whitbeck
Student ID: 5550203278
Description:
    Python API to scrape email for job application emails and synthesize all job application information into a spreadsheet.
    ConOps:
        Retrieve Emails:
            - Utilize Python library such as imaplib or poplib to retrieve and read emails.
        Parse Emails:
            - Utilize Python libraries like email or email.parser to parse the email content and extract relevant information.
            - Key information: sender, recipient, subject line, message body, datetime.
        Categorize as Job Application:
            - Use ChatGPT API to confirm email pertains to job application & status.
            - Search for keywords and reference number to confirm job application email.
        Store Information:
            - Read and write to spreadsheet tracking job applications.
            - Ensure a given application process is not duplicated but rather updates the given entry if more than one email is found.
"""
import imaplib  # connect to email server
import getpass  # get password securely
import email.parser  # parse email

def get_email(email_account):
    """Use imaplib Python library to connect to your email server and retrieve emails."""

    # Connect to email server
        # TODO implement robust email server connection, currently limited to gmail
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login to email server
    # If EMAIL_ACCOUNT is not defined, prompt user for email and assign it to EMAIL_ACCOUNT
    if not email_account:
        email_account = input("email: ")
    imap.login(email_account, getpass.getpass())

    # Select inbox
    imap.select("INBOX/iWillTeach")

    # Search for emails
    typ, data = imap.search(None, "ALL")

    # Get email IDs
    email_ids = data[0].split()

    # Iterate through email IDs
    for email_id in email_ids:
        print(f"email_id = {email_id}")

def main():
    print("Entering email tracker...")

    email_account = "kendallwhitbeck@gmail.com"

    print("get email...")
    get_email(email_account)

if __name__ == "__main__":
    main()
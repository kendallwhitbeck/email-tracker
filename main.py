"""
Program: email-tracker
Author: Kendall Whitbeck
Student ID: 5550203278
Description:
    Python API to scrape email for job application emails and synthesize all job application information into a spreadsheet.
    ConOps:
        Retrieve Emails:
            - Utilize Python library such as imaplib or poplib to retrieve and read emails.
            - Specify date range on emails to retrieve.
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

import pandas as pd  # store information in CSV

def get_email(email_account):
    """Use imaplib Python library to connect to the user's email server and retrieve emails."""

    # Connect to email server
        # TODO implement robust email server connection, currently limited to gmail
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login to email server
    # If email_account is not defined, prompt user for email and assign it to email_account
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

def parse_email(email):
    # body = email.parser("body")  # TODO
    pass

def is_job_app(email):
    """ Leverage ChatGPT API to determine if email is related to a job application."""

    is_job_app_email = False  # Initialize variable

    # TODO leverage ChatGPT API or keyword to determine if email is related to a job application; if so, set is_job_app_email = True
    is_job_app_email = 0 + 1  # TODO placeholder operation, update with functioning code

    return is_job_app_email

def job_app_exists(job_app_email, spreadsheet):
    # When passed an email regarding a job application, determine if it exists already in the spreadsheet
    pass

def update_job_app_spreadsheet(email, spreadsheet="job_app_data.csv"):
    """ When passed a valid job application email, store it in the job application tracking spreasheet.
    If passed a (path to) spreadsheet (CSV), create or write to that spreadsheet.
    If not, create it in Current Working Directory (CWD).
    Default value for spreadsheet is "data.csv" which will be created in CWD if it doesn't exist.
    """

    # # Open spreadsheet TODO Not needed if using pandas?
    # with open(spreadsheet, mode="w+") as fp:
    #     pass

    # Check to see if job_app_exists in spreadsheet by using job requisition number
     # TODO

    # Open spreadsheet as pandas dataframe
    job_app_dataframe = pd.read_csv(spreadsheet)

    # TODO: update spreadsheet using pandas
    # TODO implement code adding email entry
    # TODO start with each email being a new line regardless of entry existing already

    # Save changes back to spreadsheet
    spreadsheet = job_app_dataframe.to_csv()

    pass



def main():
    print("Entering email tracker...")

    # TODO: following line used for development, remove from final product
    email_account = "kendallwhitbeck@gmail.com"

    print("get email...")
    get_email(email_account)

if __name__ == "__main__":
    main()
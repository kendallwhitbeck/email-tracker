"""
Program: email-tracker
Author: Kendall Whitbeck
Student ID: 5550203278
Description:
    Python API to scrape email for job application emails and synthesize all job application information into a spreadsheet.
    Requires internet connection.
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
import sys
from datetime import datetime
import imaplib  # connect to email server
import getpass  # get password securely
import email  # email TODO TBD description

import pandas as pd  # store information in CSV

def get_email(email_account, since_date):
    """Use imaplib Python library to connect to the user's email server and retrieve emails."""

    # Connect to email server
        # TODO implement robust email server connection, currently limited to gmail
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login to email server
    # If email_account is not defined, prompt user for email and assign it to email_account
    if not email_account:
        email_account = input("email: ")

    # If since_date is not defined, prompt user for date and assign it to since_date  # TODO is this 'not' defined approach applicable? What happens if those arguments are not passed in?
    if not since_date:
        since_date = input("since_date ('DD-Mon-YYYY'): ")
    since_date = datetime.strftime(since_date, "%d-%b-%Y")

    # TODO temporary password, remove from deliverable # TODO DELETE FOLLOWING LINES BEFORE UPLOADING CODE TO GITHUB
    bad_practice = True  # TODO remove from deliverable
    if bad_practice:  # TODO remove from deliverable
        sys.path.append("C:/Users/kenda/Downloads")  # TODO remove from deliverable
        import BAD_PRACTICE_NEED_TO_REMOVE  # TODO remove from deliverable
        imap.login(email_account, BAD_PRACTICE_NEED_TO_REMOVE.uh_oh())  # TODO DELETE THIS BEFORE UPLOADING CODE TO GITHUB
    else:  # TODO remove from deliverable
        # TODO DELETE ABOVE LINES BEFORE UPLOADING CODE TO GITHUB
        imap.login(email_account, getpass.getpass())  # TODO fix indentation after removing above lines

    # Select inbox
    status_select, messages = imap.select("INBOX")

        # Search for emails  # TODO which search to use?
        # status_search, data_search = imap.search(None, "ALL")  # TODO remove from deliverable; keeping for reference until then
        # num_messages = int(messages[0])  # TODO remove from deliverable; keeping for reference until then

    # Search for emails newer than 'since_date' date
    search_criteria = f'(SINCE "{since_date}")'
    status_uid, data_emails_since = imap.uid('SEARCH', search_criteria)

    # Get email IDs from search result
    email_ids_since = []
    email_ids_since = data_emails_since[0].split()

    # total number of emails TODO is this needed?
    num_messages_since = len(email_ids_since)

    # Iterate through email IDs TODO
    count = 0
    for email_id in email_ids_since:

        # Fetch email message by ID
        status_uid, msg = imap.fetch(str(int(email_id)), '(RFC822)')

        # Parse email content
        for response in msg:
            if isinstance(response, tuple):
                print(f"email_id = {email_id}")  # TODO temp debug
                msg = email.message_from_bytes(response[0])

        # # TODO temporary terminal text saver
        # if count > 3:
        #     print(f"count = {count}")
        #     print("...email_ids continue...")
        #     break
        count += 1

    print(f"last email_id = {email_ids_since[-1]}")

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

    # # Open spreadsheet TODO Not needed if using pandas with default spreadsheet path?
    # with open(spreadsheet, mode="w+") as fp:
    #     pass

    # Check to see if job_app_exists in spreadsheet by using job requisition number
     # TODO Implement this capability after basic function

    # Open spreadsheet as pandas dataframe
    job_app_dataframe = pd.read_csv(spreadsheet)

    # TODO: update spreadsheet using pandas
    # TODO implement code adding email entry
    # TODO start with each email being a new line regardless of entry existing already

    # Save changes back to spreadsheet
    spreadsheet = job_app_dataframe.to_csv()



def main():
    print("Entering email tracker...")

    # TODO: following line used for development, remove from final product
    email_account = "kendallwhitbeck@gmail.com"
    # since_date = "01-11-2023"
    since_date = datetime(2023, 11, 1)

    print("get email...")
    get_email(email_account, since_date)

    # Update the spreadsheet
    # update_job_app_spreadsheet()

if __name__ == "__main__":
    main()
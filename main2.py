# main2.py
"""
This program:
    - reads emails dating back to a given date
    - determines if each email is a job application
    - stores job application information in a spreadsheet
"""

import sys
import imaplib
import email
# import email.parser
import pandas

def get_email_subject(email_msg):
    # Extract subject line from email message
    subject = ""
    try:
        subject = email_msg.get("Subject")
        subject = str(subject)
    except:
        print(f"Error extracting email subject.")
    return subject

def get_email_body(email_msg):
    # Extract message body from email message
    body = ""
    try:
        if email_msg.is_multipart():
            for part in email_msg.get_payload():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode()
        else:
            body = email_msg.get_payload(decode=True).decode()
    except:
        print("Error extracting email body.")
    return body

def get_email_sender(email_msg):
    # Extract sender from email message
    sender_str, sender_name, sender_addr = "", "", ""
    try:
        sender_str = email_msg.get("From")
        sender_name = email.utils.parseaddr(sender_str)[0]
        sender_addr = email.utils.parseaddr(sender_str)[1]
    except:
        print(f"Error extracting email sender.")
    return sender_addr  # TODO update to return sender_name too?

def get_email_datetime(email_msg):
    # Extract datetime from email message
    try:
        datetime_str = email_msg.get("Date")
        datetime_obj = email.utils.parsedate(datetime_str)  #TODO does this work better than parsedate_to_datetime?
        # datetime_obj = email.utils.parsedate_to_datetime(datetime_str)  # TODO uncomment if parsedate fails
    except:
        print(f"Error extracting email datetime.")
    return datetime_str  # TODO should I return datetime_obj instead?

def extract_email_info(email_msg):
    # # Get email_id from email_msg  TODO remove this usage of email_id?
    # email_id = email_msg.get("Message-ID")

    subject = get_email_subject(email_msg),
    body = get_email_body(email_msg),
    sender_addr = get_email_sender(email_msg),
    datetime_str = get_email_datetime(email_msg)

    return subject, body, sender_addr, datetime_str

def is_job_application(email_msg):
    """ Return True if email is a job application. """

    # Get email subject and body
    subject = get_email_subject(email_msg)
    body = get_email_body(email_msg)

    # First, filter email by keywords in subject or body
    keywords = ["job", "application", "career"]
    for keyword in keywords:
        if keyword in subject.lower() or keyword in body.lower():
            # Second, leverage ChatGPT API to determine if email is related to a job application
            return True  # TODO replace this line with another function that leverages ChatGPT API to determine if email is related to a job application
    return False

def extract_job_info(email_msg):
    """ Extract relevant job information from email message. """

    # Initialize variables
    application_num, company, position, application_status = "", "", "", ""

    # Extract email info
    subject, body, sender, datetime_str = extract_email_info(email_msg)

    # Extract job application information from email information
    pass  # TODO

    # Return job application information as a tuple
    return (application_num, company, position, application_status, datetime_str)

def main():
    # Connect to email server
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    # TODO temporary password, remove from deliverable # TODO DELETE FOLLOWING LINES BEFORE UPLOADING CODE TO GITHUB
    if True:  # TODO remove from deliverable
        sys.path.append("C:/Users/kenda/Downloads")  # TODO remove from deliverable
        import BAD_PRACTICE_NEED_TO_REMOVE  # TODO remove from deliverable
    imap.login("kendallwhitbeck@gmail.com", BAD_PRACTICE_NEED_TO_REMOVE.uh_oh())

    # Select inbox
    status, messages = imap.select("INBOX")

    # Read emails back to certain date in format DD-Mon-YYYY
    date = "01-Nov-2023"  # TODO allow user to pass in date in format DD-Mon-YYYY
    status, email_data = imap.search(None, f'SINCE {date}')

    # Parse emails to determine if each email is a job application
    job_applications = []
    count = 0
    for email_id in email_data[0].split():
        count += 1
        status, email_data = imap.fetch(email_id, "(RFC822)")
        if status == "OK":
            email_msg = email.message_from_bytes(email_data[0][1])
            # Except any error that occurs while processing email due to the large scope of potential email invalidity errors.
            try:
                if is_job_application(email_msg):
                    job_applications.append(extract_job_info(email_msg))
            except:
                print(f"Error processing email; email_id = {email_id}. Status = {status}.")
        else:
            print(f"Poor status of fetched email (email_id = {email_id}, status = {status}); skipping to next email.")
        # Indicate progress every 10 emails
        if count % 10 == 0:
            print("~", end="")

    # Store job application information in a spreadsheet
    df = pandas.DataFrame(job_applications)
    df.to_csv("job_applications.csv")

if __name__ == "__main__":
    main()
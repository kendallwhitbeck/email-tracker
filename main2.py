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

# Helper functions
def is_job_application(email_msg):
    # Extract subject line from email message
    subject = email_msg.get("Subject")
    try:
        subject = str(subject)
    except:
        print(f"Error converting subject to string; subject = {subject}")

    # Get email_id from email_msg
    email_id = email_msg.get("Message-ID")

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
        print("Error reading email message; subject = ", subject)
    # Extract datetime from email message
    datetime_str = email_msg.get("Date")
    datetime_obj = email.utils.parsedate_to_datetime(datetime_str)

    # Extract sender from email message
    sender_str = email_msg.get("From")
    sender_addr = email.utils.parseaddr(sender_str)[1]

    # Return True if email is a job application
    keywords = ["job", "application", "resume"]
    for keyword in keywords:
        if keyword in subject.lower() or keyword in body.lower():
            return True
    return False
def extract_info(email_msg):
    # TODO: extract relevant information from email message
    return {}

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
    date = "01-Nov-2023"
    status, email_data = imap.search(None, f'SINCE {date}')

    # Parse emails to determine if each email is a job application
    job_applications = []
    for email_id in email_data[0].split():
        status, email_data = imap.fetch(email_id, "(RFC822)")
        email_msg = email.message_from_bytes(email_data[0][1])
        try:
            if is_job_application(email_msg):
                job_applications.append(extract_info(email_msg))
        except:
            print(f"Error processing email; email_id = {email_id}")
        print(".", end="")

    # Store job application information in a spreadsheet
    df = pandas.DataFrame(job_applications)
    df.to_csv("job_applications.csv")

if __name__ == "__main__":
    main()
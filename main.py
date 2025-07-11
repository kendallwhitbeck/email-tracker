# main.py
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
import openai

# Facilitate development by importing API passwords upon execution instead of typing them as user input.
sys.path.append("C:/Users/kenda/Downloads")
try:
    import api_passwords
except ImportError:
    print("Error: api_passwords.py file not found.")

# Set OpenAI API key to enable use of ChatGPT API
openai.api_key = api_passwords.openai()  # NOTE to user: update to use your API key.
USE_CHATGPT = False  # NOTE to user: set `True` if you have an API key associated with a paid version of ChatGPT

def get_email_subject(email_msg):
    # Extract subject line from email message
    subject = ""
    try:
        # Get email_id from email_msg for error logging.
        email_id = email_msg.get("Message-ID")
        # Extract subject from email_msg
        subject = str(email_msg.get("Subject"))
    except:
        print(f"\nError extracting email subject, email_id = {email_id}.")
    return subject

def get_email_body(email_msg):
    """ Extract message body from email message. """

    body = ""
    try:
        # Get email_id from email_msg for error logging.
        email_id = email_msg.get("Message-ID")
        # Account for multipart emails
        if email_msg.is_multipart():
            for part in email_msg.get_payload():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode()
        else:
            body = email_msg.get_payload(decode=True).decode()
    except:
        print(f"\nError extracting email body, email_id = {email_id}.")
    return body

def get_email_sender(email_msg):
    """Extract sender from email message. """

    sender_str, sender_name, sender_addr = "", "", ""
    try:
        # Get email_id from email_msg for error logging.
        email_id = email_msg.get("Message-ID")
        # Extract sender name and email address from email_msg
        sender_str = email_msg.get("From")
        sender_name = email.utils.parseaddr(sender_str)[0]
        sender_addr = email.utils.parseaddr(sender_str)[1]
    except:
        print(f"Error extracting email sender, email_id = {email_id}.")
    return sender_name, sender_addr

def get_email_date_time(email_msg):
    """ Extract datetime from email message. """

    try:
        # Get email_id from email_msg for error logging.
        email_id = email_msg.get("Message-ID")

        datetime_str = email_msg.get("Date")

        # Extract date string
        date_parts = datetime_str.split()[:3] # Extract date from email_msg
        date_str = " ".join(date_parts) # Join date parts to form a string

        # Extract time string
        time_parts = datetime_str.split()[4:] # Extract time of day and timezone from email_msg
        time_str = " ".join(time_parts) # Join time parts to form a string

        # Extract datetime object TODO is this needed?
        datetime_obj = email.utils.parsedate(datetime_str)  #TODO is datetime_obj needed? does parsedate work better than parsedate_to_datetime?
        # datetime_obj = email.utils.parsedate_to_datetime(datetime_str)  # TODO uncomment if parsedate fails
    except:
        print(f"Error extracting email datetime, email_id = {email_id}.")
    return date_str, time_str  # TODO should I return datetime_obj instead?

def extract_email_info(email_msg):
    """ Extract relevant email information from email message. """

    subject = get_email_subject(email_msg),
    body = get_email_body(email_msg),
    sender_name, sender_addr = get_email_sender(email_msg)
    date_str, time_str = get_email_date_time(email_msg)

    return subject, body, sender_name, sender_addr, date_str, time_str  # TODO make robust to changing order or attributes

def is_job_application(email_msg):
    """ Return True if email is a job application. """

    # Get email subject and body
    subject = get_email_subject(email_msg)
    body = get_email_body(email_msg)
    sender_name, sender_addr = get_email_sender(email_msg)

    # First, filter email by keywords in subject or body to speed up processing.
    keywords = ["job", "application", "career"]
    # keywords = ["job application", "open position"]  # TODO determine more specific keywords for job applications if not using ChatGPT
    for keyword in keywords:
        if keyword in subject.lower() or keyword in body.lower():
            if USE_CHATGPT:
                # Second, leverage ChatGPT API to fully determine if email is related to a job application.
                print(f"Keyword match: {keyword} in subject or body. Asking ChatGPT if the email is a job application...")
                prompt = f"Is this an email regarding a job application?\n\nSender: {sender_name} <{sender_addr}>\n\n.Subject: {subject}.\n\nBody: {body}."
                response = openai.Completion.create(
                    # NOTE to user: uncomment your preferred ChatGPT model ("engine")
                    engine="gpt-3.5-turbo",
                    # engine="gpt-3.5-turbo-instruct",
                    # engine="gpt-4",
                    # engine="/v1/models",
                    prompt=prompt,
                    max_tokens=50
                )
                answer = response.choices[0].text.strip().lower()
                if "yes" in answer:
                    return True
            return True
    return False

def extract_job_info(email_msg):
    """ Extract relevant job information from email message. """

    # Initialize variables
    application_num, company, position, application_status = "", "", "", ""

    # Extract email info
    subject, body, sender_name, sender_addr, date_str, time_str = extract_email_info(email_msg)  # TODO make robust to changing order or attributes

    # Extract job application information from email information using ChatGPT API
    application_num = "application_num"  # TODO temporary placeholder
    company = sender_name  # TODO temporary placeholder
    position = "position"  # TODO temporary placeholder
    application_status = "application_status"  # TODO temporary placeholder
    pass  # TODO implement ChatGPT API code to extract job application information

    # Return job application information as a tuple
    return (application_num, company, position, application_status, sender_name, subject, date_str, time_str)  # TODO make robust to changing order or attributes

def main():
    """ Main function to login to email server, collect and process emails, store job application information. """

    # Set debug mode
    debug=True  # TODO use for development
    # debug=False  # TODO use for full list
    if debug:
        dbg_lim = 50
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n",
              f"WARNING: YOU ARE IN DEBUG MODE. ONLY {dbg_lim} EMAILS WILL BE PROCESSED.\n",
              "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # Connect to email server TODO should I modularize the email server connection code?
    imap = imaplib.IMAP4_SSL("imap.gmail.com")  # TODO: make robust to email server domain
    imap.login("kendallwhitbeck@gmail.com", api_passwords.gmail())  # NOTE to user: update to use your email address and API key

    # Select inbox
    status, messages = imap.select("INBOX")  # TODO can probably update this to search specific `Labels` in gmail

    # Read emails back to certain date in format DD-Mon-YYYY
    date = "01-Nov-2023"  # TODO allow user to pass in date in format DD-Mon-YYYY
    # date = "23-May-2024"  # TODO allow user to pass in date in format DD-Mon-YYYY
    # search_criteria = f'(SINCE "{date}" BODY "job application status")'  # TODO update search to return emails that are shown when searching for {"job" application status}
    # status, email_data = imap.uid('SEARCH', search_criteria)  # TODO update search to return emails that are shown when searching for {"job" application status}
    status, email_data = imap.search(None, f'SINCE {date}')  # NOTE will 'mark read' any matching email results.

    # Initialize email parsing variables.
    job_applications = []
    count = 0
    email_ids = email_data[0].split()
    progress_symbol = "%"

    # Parse emails to determine if each email is a job application
    print(f"Processing {len(email_ids)} emails, one '{progress_symbol}' is ten emails...")
    for email_id in email_ids:
        count += 1
        # Fetch given email data from server using RFC 822 (standard email message) format.
        status, email_data = imap.fetch(email_id, "(RFC822)")
        if status == "OK":
            if email_data[0] is None:
                print(f"Error fetching email (email_id = {email_id}); skipping to next email.")
                continue
            # Extract email message from email bytes data
            email_msg = email.message_from_bytes(email_data[0][1])
            if is_job_application(email_msg):
                # Extract relevant job information from email and append to job_applications list.
                job_applications.append(extract_job_info(email_msg))
        else:
            print(f"Poor status of fetched email (email_id = {email_id}, status = {status}); skipping to next email.")

        # Indicate progress every x emails
        x = 10
        if count % x == 0:
            print(f"{progress_symbol} ", end="")

        # If debugging, stop after processing debug limit number of emails
        if debug:
            if count == dbg_lim:
                print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n",
                     f"WARNING: YOU ARE IN DEBUG MODE. STOPPED AFTER {count} EMAILS.\n",
                      "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                break

    # Convert list of job application information to pandas dataframe.
    column_names = ["application_num", "company", "position", "application_status", "sender_name", "subject", "date_str", "time_str"]  # TODO make robust to changing order or attributes
    job_app_df = pandas.DataFrame(job_applications, columns=column_names)

    # Store job application information in a csv spreadsheet
    file = "job_applications.csv"
    try:
        job_app_df.to_csv(file, index=True)  # TODO date is coming out as {"Day, D Mon"} and time is stored without quotes
    except PermissionError as e:
        print(f"Error storing job application information in a spreadsheet: {e}.\nENSURE THE FOLLOWING FILE IS CLOSED!\n----> {file} <----")

    # Close connection to email server
    imap.close()
    imap.logout()
    print("Done.")

if __name__ == "__main__":
    main()
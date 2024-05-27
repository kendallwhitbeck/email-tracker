# email-tracker
Python API to scrape email for job application emails and synthesize all job application information into a spreadsheet.

Usage:
Download all files to same directory.
Run main.py, e.g.:
    $ py main.py

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

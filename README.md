# email-tracker
Python API to scrape email for job application emails and synthesize all job application information into a spreadsheet.

ConOps:
1.	Retrieve Emails:
    a.	Utilize Python library such as imaplib or poplib to retrieve and read emails.
3.	Parse Emails:
  a.	Utilize Python libraries like email or email.parser to parse the email content and extract relevant information.
  b.	Key information: sender, recipient, subject line, message body, datetime.
4.	Categorize as Job Application:
  a.	Use ChatGPT API to confirm email pertains to job application & status.
  b.	Search for keywords and reference number to confirm job application email.
5.	Store Information:
  a.	Read and write to spreadsheet tracking job applications.
  b.	Ensure a given application process is not duplicated but rather updates the given entry if more than one email is found.

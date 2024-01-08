from exchangelib import Credentials, Account, DELEGATE, HTMLBody, Message

# Replace these values with your Outlook account details
email_address = 'patadoc@outlook.com'
password = '3Engineers'
recipient_email = 'priscandiritu@outlook.com'
subject = 'Test Email'
body = 'This is a test email sent from Python using exchangelib.'

# Set up credentials
credentials = Credentials(email_address, password)

# Connect to the Outlook account
account = Account(email_address, credentials=credentials, autodiscover=True, access_type=DELEGATE)

# Create an email message
email = Message(
    account=account,
    subject=subject,
    body=HTMLBody(body),
    to_recipients=[recipient_email]
)

# Send the email
email.send()

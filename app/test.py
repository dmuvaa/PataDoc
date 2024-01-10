from exchangelib import Credentials, Account, DELEGATE, HTMLBody, Message
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.', '.env'))
# Replace these values with your Outlook account details
email_address = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
recipient_email = 'transcriberandwriter@gmail.com'
subject = 'Test Email'
body = 'This is a test email sent from Python using exchangelib.'

# Set up credentials
credentials = Credentials(email_address, password)

# Connect to the Outlook account
account = Account(email_address, credentials=credentials, autodiscover=True, access_type=DELEGATE)

#Create an email message
email = Message(
    account=account,
    subject=subject,
    body=HTMLBody(body),
    to_recipients=[recipient_email]
)

# Send the email
email.send()
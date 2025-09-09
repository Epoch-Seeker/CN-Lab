import smtplib
import logging
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
load_dotenv()

SMTP_EMAIL = os.getenv('SMTP_EMAIL')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

# Configure logging
logging.basicConfig(
    filename='smtp_communication.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def send_test_email(smtp_server, port, sender_email, sender_password, recipient_email):
    try:
        # Prepare the email content
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = 'Test Email from Python SMTP Program'

        body = "Hello,\n\nThis is a test email sent using Python's smtplib.\n\nRegards,\nPython Script"
        message.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server
        with smtplib.SMTP(smtp_server, port) as server:
            server.set_debuglevel(1)  # Enable debug output to stdout

            logging.info(f"Connecting to SMTP server: {smtp_server}:{port}")
            server.ehlo()

            # For TLS (recommended)
            if port == 587:
                server.starttls()
                server.ehlo()

            logging.info("Logging in to SMTP server...")
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, recipient_email, message.as_string())
            logging.info(f"Email successfully sent to {recipient_email}")

            print("Email sent successfully!")

    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        print(f"Error sending email: {e}")

def main():
    # SMTP configuration (example uses Gmail)
    smtp_server = 'smtp.gmail.com'
    port = 587  # Use 465 for SSL, 587 for TLS

    sender_email = SMTP_EMAIL
    sender_password = SMTP_PASSWORD  # Use an App Password, not your real password

    recipient_email = 'sunnykumar173205@gmail.com'

    send_test_email(smtp_server, port, sender_email, sender_password, recipient_email)

if __name__ == "__main__":
    main()

import smtplib
import time
import schedule
from email.message import EmailMessage
import os

# 1. Email configuration (use environment variables for security)
# Set these environment variables in your system: EMAIL_ADDRESS, EMAIL_PASSWORD
SENDER_EMAIL = os.environ.get('EMAIL_ADDRESS')
SENDER_PASSWORD = os.environ.get('EMAIL_PASSWORD')
SMTP_SERVER = 'smtp.gmail.com' # Replace with your SMTP server (e.g., smtp.outlook.com)
SMTP_PORT = 587 # Port for TLS (587) or SSL (465)

# In a real application, you would fetch subscribers from a database or a CSV file
def get_subscribers():
    """Fetches the list of email recipients."""
    # Example list of recipients
    return ["recipient1@example.com", "recipient2@example.com"]

def send_daily_email():
    """Composes and sends the daily email to all subscribers."""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Error: Email credentials not set in environment variables.")
        return

    recipients = get_subscribers()
    subject = "Today's Word of the day is ready!"
    body = "This is your automated daily email update. Have a great day!"

    for recipient in recipients:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient

        try:
            # Connect to the SMTP server and send the email
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls() # Secure the connection with TLS
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
                print(f"Email sent successfully to {recipient}")
        except Exception as e:
            print(f"Failed to send email to {recipient}. Error: {e}")

# 2. Schedule the email to run daily
# This example runs the function every day at 8:00 AM
schedule.every().day.at("07:00").do(send_daily_email)

print("Email scheduler started. Waiting for the scheduled time...")

# 3. Keep the script running to check the schedule
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(60) # Wait 60 seconds before checking the schedule again

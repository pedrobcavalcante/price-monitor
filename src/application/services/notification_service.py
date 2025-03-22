from typing import List
from smtplib import SMTP
from email.mime.text import MIMEText

class NotificationService:
    def __init__(self, email_recipients: List[str], smtp_server: str, smtp_port: int, smtp_user: str, smtp_password: str):
        self.email_recipients = email_recipients
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password

    def send_notification(self, subject: str, message: str):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.smtp_user
        msg['To'] = ', '.join(self.email_recipients)

        with SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.smtp_user, self.email_recipients, msg.as_string())

    def notify_price_change(self, product_name: str, old_price: float, new_price: float):
        subject = f'Price Change Alert: {product_name}'
        message = f'The price for {product_name} has changed from {old_price} to {new_price}.'
        self.send_notification(subject, message)

    def notify_new_posting(self, product_name: str, product_url: str):
        subject = f'New Posting Alert: {product_name}'
        message = f'A new posting for {product_name} has been found: {product_url}'
        self.send_notification(subject, message)
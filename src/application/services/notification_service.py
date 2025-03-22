import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from loguru import logger

class NotificationService:
    def __init__(
        self,
        email_recipients: List[str] = None,
        smtp_server: str = None,
        smtp_port: int = 587,
        smtp_user: str = None,
        smtp_password: str = None
    ):
        """
        Initialize notification service
        
        Args:
            email_recipients: List of email recipients
            smtp_server: SMTP server address
            smtp_port: SMTP server port
            smtp_user: SMTP username
            smtp_password: SMTP password
        """
        self.email_recipients = email_recipients or []
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        
    def notify(self, message: str, url: Optional[str] = None) -> bool:
        """
        Send a notification
        
        Args:
            message: Notification message
            url: Optional URL to include in the notification
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        try:
            logger.info(f"Notification: {message}")
            
            # If email configuration is provided, send email
            if self.smtp_server and self.smtp_user and self.email_recipients:
                self._send_email(message, url)
            
            return True
        except Exception as e:
            logger.error(f"Failed to send notification: {str(e)}")
            return False
            
    def _send_email(self, message: str, url: Optional[str] = None) -> None:
        """
        Send an email notification
        
        Args:
            message: Email message
            url: Optional URL to include in the email
        """
        try:
            if not self.email_recipients:
                return
                
            msg = MIMEMultipart()
            msg['Subject'] = 'OLX Price Monitor Alert'
            msg['From'] = self.smtp_user
            msg['To'] = ', '.join(self.email_recipients)
            
            body = f"{message}\n\n"
            if url:
                body += f"Link: {url}"
                
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email notification sent to {self.email_recipients}")
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
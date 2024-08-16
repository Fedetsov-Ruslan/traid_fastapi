import smtplib
import logging
from email.message import EmailMessage

from celery import Celery
from src.config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD


celery = Celery('tasks', broker='redis://localhost:6379', broker_connection_retry_on_startup = True)

def get_email_template_dashboard(username:str):
    email = EmailMessage()
    email['Subject'] = 'Dashboard'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER
    email.set_content('Hello, its dashboard')
    return email

@celery.task
def send_email_report_dashboard(username:str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        try:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(email)
        except smtplib.SMTPAuthenticationError as e:
            logging.error(f"SMTP Authentication Error: {e}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
    
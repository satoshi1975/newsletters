"""celery tasks"""
from .mail import send_email
from email_sender.celery import app

@app.task
def send_delayed_email(email_data):
    """task for deferred mailing"""
    send_email_task.delay(email_data)

@app.task
def send_email_task(email_data):
    """task for background sending emails"""
    send_email(email_data)

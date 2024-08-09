import smtplib, logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

LOGGER = logging.getLogger('Gmail Notify')

import os
GMAIL_ENABLE                    = int(os.environ.get('GMAIL_ENABLE', '0'))
GMAIL_APPLICATION_TOKEN         = str(os.environ.get('GMAIL_APPLICATION_TOKEN', ''))
SENDER_GMAIL                    = str(os.environ.get('SENDER_GMAIL', ''))
RECEIVER_EMAIL                  = str(os.environ.get('RECEIVER_EMAIL', ''))

def notify(method='', message =''):
    if GMAIL_ENABLE == 0:
        LOGGER.info('Gmail notify is disable '+message)
        return False

    if method == 'done':
        gmail_content = MIMEMultipart()

        gmail_content["subject"] = '[INFO] Running neopets helper'
        gmail_content["from"] = SENDER_GMAIL
        gmail_content["to"] = RECEIVER_EMAIL
        gmail_content.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP(host='smtp.gmail.com', port='587') as smtp:
            try:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(SENDER_GMAIL, GMAIL_APPLICATION_TOKEN)
                LOGGER.info('start sending email')
                smtp.send_message(gmail_content)
            except:
                LOGGER.error('start send failed')
                raise

    elif method == 'error':
        gmail_content = MIMEMultipart()

        gmail_content["subject"] = '[ERROR] Login failed neopets helper'
        gmail_content["from"] = SENDER_GMAIL
        gmail_content["to"] = RECEIVER_EMAIL
        gmail_content.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP(host='smtp.gmail.com', port='587') as smtp:
            try:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(SENDER_GMAIL, GMAIL_APPLICATION_TOKEN)
                LOGGER.info('error sending email')
                smtp.send_message(gmail_content)
            except:
                LOGGER.error('error send failed')
                raise

from email.mime.text import MIMEText
import smtplib
import hashlib
from pydantic import ValidationError


def send_email(body: str, recipients):
    msg = MIMEText(body)
    msg['Subject'] = 'Register confirm'
    msg['From'] = "buskomaksym08@gmail.com"
    msg['To'] = recipients
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login("logiconnect.supp@gmail.com", "ljzp avgg lpkb ozvr")
        smtp_server.sendmail("logiconnect.supp@gmail.com", recipients, msg.as_string())


def hashing(x): return hashlib.sha256(x.encode('utf-8')).hexdigest()


def check_model(data: dict, model):
    try:
        model(**data)
        return True
    except ValidationError:
        return False

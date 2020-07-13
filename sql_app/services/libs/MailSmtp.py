import smtplib
from fastapi.templating import Jinja2Templates
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

class MailSmtpException(Exception):
    def __init__(self,message: str):
        super().__init__(message)

class MailSmtp:
    _SMTP_SERVER = "smtp.mailtrap.io"
    _PORT = "2525"
    _EMAIL = "0a1a83ec6a5ac4"
    _PASSWORD = "aa80a2457da80a"
    _USE_SSL = "false"

    _templates = Jinja2Templates(directory="services/templates")

    @classmethod
    def send_email(cls,email: List[str],subject: str,html: str,**param) -> None:
        if not cls._EMAIL: raise MailSmtpException('Email for sender not found')
        if not cls._PASSWORD: raise MailSmtpException('Password for email not found')

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = 'dont-reply'
        msg['To'] = ','.join(email)

        template = cls._templates.get_template(html)
        html = template.render(**param)

        msg.attach(MIMEText(html,'html'))
        # Try to log in to server smtp
        try:
            if cls._USE_SSL == 'true': server = smtplib.SMTP_SSL(cls._SMTP_SERVER,cls._PORT)
            else: server = smtplib.SMTP(cls._SMTP_SERVER,cls._PORT)
        except smtplib.SMTPException as e:
            raise MailSmtpException(e)

        # login and send email
        try:
            server.login(cls._EMAIL,cls._PASSWORD)
            server.sendmail(cls._EMAIL,email,msg.as_string())
            server.quit()
        except smtplib.SMTPException as e:
            raise MailSmtpException(e)

import smtplib
import ssl
from email.message import EmailMessage
from smtplib import SMTP_SSL

ROOT = ""
PASSWORD = ""
email = EmailMessage()
email["From"] = ROOT
email["To"] = ""
email["Subject"] = "SAGW - Восстановление аккаунта "
MESSAGE_RESTORE_ACCOUNT = """
Текст
Текст
Текст
"""
email.set_content(MESSAGE_RESTORE_ACCOUNT)

def send_email(cls, mail: str) -> None:
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            server.login(ROOT, PASSWORD)
            server.sendmail(ROOT, mail, email.as_string())
    except:
        return print("Не удалость отправить сообщение!")

    return print("Сообщение отправлено успешно")

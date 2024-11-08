import email.mime.multipart
import email.mime.base
from email.mime.text import MIMEText
import email.encoders
import email
import ssl
import smtplib
from config import EMAIL, EMAIL_PASS, EMAIL_PORT, EMAIL_HOST
from threading import Thread
import random


def send_simple_mail_task(email_receptor:str, content:str, asunto:str):
    t = Thread(target=send_simple_mail, args=(email_receptor, content, asunto,))
    t.start()

def send_simple_mail(email_receptor:str, content:str, asunto:str):

    em = email.mime.multipart.MIMEMultipart()
    em["From"] = EMAIL
    em["To"] = email_receptor
    em["Subject"] = asunto
    em.attach(MIMEText(content))

    contexto = ssl.create_default_context()

    with smtplib.SMTP_SSL(host=EMAIL_HOST, port=EMAIL_PORT, context=contexto) as smtp:
        smtp.login(EMAIL, EMAIL_PASS)
        smtp.sendmail(EMAIL, email_receptor, em.as_string())

def generate_password(email:str):
    
    avaliable_characters = ['1','2','3','4','5','6','7','8','9','0']
    generated = ""
    for i in range(10):
        generated += avaliable_characters[random.randrange(avaliable_characters.__len__())]
        
    send_credentials(email=email, password=generated)
    
    return generated


def send_credentials(email:str, password:str):

    txt = f"""
    Tu contraseña ah sido cambiada.
    ------------------------------------------
    Su información de inicio de sesion es:
    
    Usuario: {email}
    
    Contraseña: {password}
    """
    
    send_simple_mail_task(email_receptor=email, content=txt, asunto="Link CopecFlux")
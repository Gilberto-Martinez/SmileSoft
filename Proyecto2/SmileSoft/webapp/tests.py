# from django.test import TestCase
import smtplib
from email.mime.text import MIMEText
# from SmileSoft.settings import *

def send_mail():
    try:
        # mailServer = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        print(mailServer.ehlo()) 
        mailServer.starttls()
        print(mailServer.ehlo())
        # mailServer.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        mailServer.login('smilesoftteam@gmail.com', 'AIzaSyAsAtTpGYP02DkbUyHLYUXjIDyiISn7FAY')
        print('Conectado..')

        # Construimos el mensaje simple
        mensaje = MIMEText("""Este es el mensaje
        de las narices""")
        mensaje['From']="smilesoftteam@gmail.com"
        mensaje['To']="martinez@gmail.com"
        mensaje['Subject']="Tienes un correo"
    except Exception as e:
        print(e)

send_mail()
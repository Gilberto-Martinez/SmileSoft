from .google_api import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo(email,nombre_usuario,password):
    CLIENT_SECRET_FILE = "webapp/static/json/trchatbot.json"
    API_NAME = "gmail"
    API_VERSION = "v1"
    SCOPES = ["https://mail.google.com/"]

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    emailMsg ="""Su usuario ha sido generado exitosamente, ingrese los siguientes datos para iniciar sesion:
                \n Usuario: """ + nombre_usuario +"""\n Contraseña: """+ password +"""
                \n SmileSoft"""
    mimeMessage = MIMEMultipart()
    mimeMessage["to"] = email
    mimeMessage["subject"] = "Mensaje de confirmación"  #titulo
    mimeMessage.attach(MIMEText(emailMsg, "plain"))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(userId = "me", body = {"raw": raw_string}).execute()
    print("--------------ENVIO DE CORREO ELECTRONICO")
    print("Correo electronico: "+ email)
    print("Usuario: "+ nombre_usuario)
    print("Contraseña: "+password)
    print(message)

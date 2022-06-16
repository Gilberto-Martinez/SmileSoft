import webapp.google_api
from webapp.google_api import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template import loader

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

def enviar_link_reseteo(email, nombre_usuario,password):
    CLIENT_SECRET_FILE = "webapp/static/json/trchatbot.json"
    API_NAME = "gmail"
    API_VERSION = "v1"
    SCOPES = ["https://mail.google.com/"]

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    # you = "martinezcanhete@gmail.com"

    # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    # html = loader.render_to_string(email_template_name)
    html = """\
        <html>
        <head></head>
        <body>
            <p>Solicitaste reestablecimiento de contraseña.
            <br>
            Tu nueva <b>contraseña</b> es: """+password+"""
            <br>
            Tu <b>usuario</b> es:  """+nombre_usuario+""".
            <br>
            <br>
            Para iniciar sesión ingresa <a href="http://127.0.0.1:8000/">aqui</a> e ingresa estos datos.
            <br>
            <br>
            Sugerimos que una vez iniciado sesión cambie su contraseña por motivos de seguridad.
            <br>
            <br>
            <i>SmileSoft</i>
            </p>
        </body>
        </html>
        """

    # Create message container - the correct MIME type is multipart/alternative.
    mimeMessage = MIMEMultipart('alternative')
    mimeMessage['To'] = email
    mimeMessage['Subject'] = "Reestablecimiento de contraseña"
    mimeMessage.attach(MIMEText(html, "html"))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(userId = "me", body = {"raw": raw_string}).execute()
    print("-----------ENVIO DE CORREO ELECTRONICO HTML----------")
    print(message)
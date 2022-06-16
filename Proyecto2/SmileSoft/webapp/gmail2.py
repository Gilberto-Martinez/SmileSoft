import google_api
from google_api import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail.message import EmailMultiAlternatives

def enviar_link_reseteo(request):
    CLIENT_SECRET_FILE = "webapp/static/json/trchatbot.json"
    API_NAME = "gmail"
    API_VERSION = "v1"
    SCOPES = ["https://mail.google.com/"]

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    # me == my email address
    # you == recipient's email address
    me = "teamsmilesoft@gmail.com"
    you = "martinezcanhete@gmail.com"

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Link"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = """\
    <html>
    <head></head>
    <body>
        <p>Hi!<br>
        How are you?<br>
        Here is the <a href="http://www.python.org">link</a> you wanted.
        </p>
    </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    raw_string = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    message = service.users().messages().send(userId = "me", body = {"raw": raw_string}).execute()
    print("--------------ENVIO DE CORREO ELECTRONICO HTML")
    print(message)

enviar_link_reseteo()
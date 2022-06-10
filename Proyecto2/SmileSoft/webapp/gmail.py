from google_api import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# import json
import os
from pathlib import Path
# from SmileSoft.settings import BASE_DIR
# from static.utils.config.my_json import *

BASE_DIR = Path(__file__).resolve().parent.parent

# json_data = os.path.join(BASE_DIR, 'static', "json/trchatbot.json")
# data = open(json_data,'r')

# CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'static', "json/trchatbot.json")
CLIENT_SECRET_FILE = "json/trchatbot.json"
API_NAME = "gmail"
API_VERSION = "v1"
SCOPES = ["https://mail.google.com/"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

emailMsg ="Eyyy esto es una prueba python(mandando mensaje desde python"
mimeMessage = MIMEMultipart()
mimeMessage["to"] = "martinezcanhete@gmail.com"
mimeMessage["subject"] = "Otra pruebaaaaaaa"  #titulo
mimeMessage.attach(MIMEText(emailMsg, "plain"))
raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

message = service.users().messages().send(userId = "me", body = {"raw": raw_string}).execute()
print(message)
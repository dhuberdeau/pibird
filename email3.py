import time
import smtplib 
import email
import email.mime.application
from picamera2 import Picamera2, Preview


# init Raspberry Pi Camera
camera = Picamera2()
config = camera.create_preview_configuration({"size": (2592, 1944)})
camera.configure(config)

# take picture:
camera.start_preview(Preview.QTGL)
camera.start()
time.sleep(2)
camera.capture_file("test_attmt.jpg")
camera.stop_preview()
camera.stop()

# provide credentials
SMTP_SERVER = 'smtp.gmail.com' #Email Server (don't change!)
SMTP_PORT = 587 #Server Port (don't change!)
GMAIL_USERNAME = 'birdeye033@gmail.com' #change this to match your gmail account
GMAIL_PASSWORD = 'vtsavwsgafnfmxkb' 
recipient = 'birdeye@myyahoo.com'

#login = 'birdeye@myyahoo.com'
#password = getpass('Password for "%s": ' % login)
#password = 'fidelio0()'

headers = ["From: " + GMAIL_USERNAME, "Subject: " + 'Test', "To: " + 'birdeye@myyahoo.com',
                   "MIME-Version: 1.0", "Content-Type: text/html"]
headers = "\r\n".join(headers)
content = "This is a test of smtp service."

#Connect to Gmail Server
msg = email.mime.Multipart.MIMEMultipart()
msg['Subject'] = 'Image attachment test'
msg['From'] = 'birdeye033@gmail.com'
msg['To'] = 'birdeye@myyahoo.com'

body = email.mime.Text.MIMEText("""Sunday June 4 2023 12:30""")
msg.attach(body)



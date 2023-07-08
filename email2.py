import smtplib 

# init Raspberry Pi Camera


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
session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
session.ehlo()
session.starttls()
session.ehlo()

#Login to Gmail
session.login(GMAIL_USERNAME, GMAIL_PASSWORD)

#Send Email & Exit
session.sendmail(GMAIL_USERNAME, recipient, headers + "\r\n\r\n" + content)
session.quit

# create message
#msg = MIMEText('Test body', 'plain', 'utf-8')
#msg['Subject'] = Header('Test', 'utf-8')
#msg['From'] = login
#msg['To'] = 'david.huberdeau@gmail.com'

# send it   
#s = SMTP_SSL('smtp.mail.yahoo.com', timeout=10)

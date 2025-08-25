import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

# --- Load env variables ---
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

# --- Read emails from email.txt ---
users = []
with open("email.txt", "r") as f:
    for line in f:
        line = line.strip()
        if line:  # skip empty lines
            email, name = line.split(",", 1)  # split only on first comma
            users.append((email.strip(), name.strip()))

# --- Connect to SMTP using TLS ---
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.ehlo()
server.starttls()
server.ehlo()
server.login(SMTP_USER, SMTP_PASS)

# --- Send emails ---
for email, name in users:
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = email
    msg['Subject'] = "Good Night!"
    msg.attach(MIMEText(f"Hi {name},\n\nWishing you a peaceful night ahead!", 'plain'))
    server.sendmail(SMTP_USER, email, msg.as_string())
    print(f"Email sent to {name} ({email})")

server.quit()
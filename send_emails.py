import os
from dotenv import load_dotenv
import psycopg2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- Load env variables ---
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

# --- Connect to PostgreSQL ---
conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cur = conn.cursor()
cur.execute('SELECT email, name FROM "User";')
users = cur.fetchall()
cur.close()
conn.close()

# --- Connect to SMTP server ---
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(SMTP_USER, SMTP_PASS)

# --- Send emails ---
for email, name in users:
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = email
    msg['Subject'] = "Hello from Python!"

    body = f"Hi {name},\n\nThis is a test email from Python automation."
    msg.attach(MIMEText(body, 'plain'))

    server.sendmail(SMTP_USER, email, msg.as_string())
    print(f"Email sent to {name} ({email})")

server.quit()
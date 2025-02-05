from intelxapi import intelx
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import time
from datetime import datetime, timedelta

intelx = intelx('dein_API_key')
target = 'Test_Email@gmail.com'
email_sender = 'deine_Email_Adresse@gmail.com'
email_receiver = 'Empfänger_Email_Adresse@gmail.com'
email_password = 'dein_Email_Passwort'

def get_pastes(target):
    search = intelx.search(target)
    record_count = len(search['records'])
    if record_count > 0:
        send_email('IntelXChecker -Leak deiner Email-Adresse', f"Bei deiner Email-Adresse {target} gab es einen Datenleak!")
    print(f"Found {record_count} records for {target} in bucket 'pastes'")

def get_leaks(target):
    search = intelx.search(target, buckets=['leaks.public', 'leaks.private'], maxresults=2000)
    record_count = len(search['records'])
    if record_count > 0:
        send_email('IntelXChecker -Leak deiner Email-Adresse', f"Bei deiner Email-Adresse {target} gab es einen Datenpaste!")
    print(f"Found {record_count} records for {target} in bucket 'leaks'")


def get_darknet(target):
    search = intelx.search(target, buckets=['darknet'], maxresults=2000)
    record_count = len(search['records'])
    if record_count > 0:
        send_email('IntelXChecker -Leak deiner Email-Adresse', f"Bei deiner Email-Adresse {target} gab es eine Alarmierung für das Darknet!")
    print(f"Found {record_count} records for {target} in bucket 'darknet'")

def send_email(subject, body):
    """
    Sende eine E-Mail mit dem gegebenen Betreff und Inhalt.
    """
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Gmail SMTP verwenden (andere Provider erfordern möglicherweise Anpassungen)
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.send_message(msg)
        print("E-Mail wurde erfolgreich gesendet.")
    except Exception as e:
        print(f"Fehler beim Senden der E-Mail: {e}")

def execute_task():
    get_leaks(target)
    get_pastes(target)
    get_darknet(target)

if __name__ == '__main__':
    next_run = datetime.now() + timedelta(days=1)
    next_run = next_run.replace(hour=8, minute=0, second=0, microsecond=0)  # Führe es z. B. um 8:00 Uhr aus

    while True:
        now = datetime.now()
        if now >= next_run:
            execute_task()
            next_run += timedelta(days=1)
        time.sleep(60)  # Überprüfe alle 60 Sekunden
    

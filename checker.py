from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, timedelta

# Deine E-Mail-Adresse
email = "richter.helena@web.de"

# Webdriver-Setup mit optionalem Headless-Modus
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Optional: Unsichtbarer Modus

def execute_task():
    """Führt die Aufgabe aus."""
    driver = webdriver.Chrome(options=options)
    try:
        # Öffne die Website
        driver.get("https://sec.hpi.de/ilc/?lang=de")

        # E-Mail-Feld finden und E-Mail eingeben
        email_input = driver.find_element(By.NAME, "email")
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)

        print(f"Task ausgeführt um: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Warte, falls notwendig
        time.sleep(5)

    finally:
        driver.quit()

def main():
    """Läuft kontinuierlich und führt die Aufgabe einmal pro Tag aus."""
    next_run = datetime.now() + timedelta(days=1)
    next_run = next_run.replace(hour=8, minute=0, second=0, microsecond=0)  # Führe es z. B. um 8:00 Uhr aus

    while True:
        now = datetime.now()
        if now >= next_run:
            execute_task()
            next_run += timedelta(days=1)
        time.sleep(60)  # Überprüfe alle 60 Sekunden

if __name__ == "__main__":
    main()

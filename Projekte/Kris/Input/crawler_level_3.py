import requests
from bs4 import BeautifulSoup
import os

# Zielverzeichnis definieren
directory = "F:/Prog/ATD/Projekte/Kris/Output"
os.makedirs(directory, exist_ok=True)

# Datei mit den Links
file_path = r"F:/Prog/ATD/Projekte/Kris/Output/level_2_output.txt"

# Zeile 3 (Index 2) lesen
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

selected_line = lines[2].strip()  # Zeile bereinigen (entfernt \n, Leerzeichen)

# Link extrahieren (nach dem "URL: ")
url_part = selected_line.split("URL: ")[-1].strip()

# Letzter Teil des Links als Dateiname
url_end = url_part.rstrip('/').split('/')[-1]  # z. B. 'magazine'
filename = os.path.join(directory, f"{url_end}.html")

def scrape_and_save(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        html_text = soup.prettify()

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_text)

        print(f"Inhalt erfolgreich in {filename} gespeichert.")
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Webseite: {e}")

# URL ohne Zeilenumbruch
scrape_and_save(url_part, filename)

# Fügt die Inhalte der der txt Datei als variablen ein und ruft diese Links auf und speichert sie als html dateien 


import requests
from bs4 import BeautifulSoup
import os
import re

# Zielverzeichnis definieren
directory = "F:/Prog/ATD/Projekte/Kris/Output"
os.makedirs(directory, exist_ok=True)

# Datei mit den Links
file_path = os.path.join(directory, "crawler2.txt")

# URL aus beliebigem Text extrahieren (Regex)
def extract_url(text):
    match = re.search(r'https?://[^\s,]+', text)
    return match.group(0) if match else None

# HTML jeder URL speichern
def scrape_and_save(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        html_text = soup.prettify()

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_text)

        print(f"[✓] Gespeichert: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"[!] Fehler bei {url}: {e}")

# Alle Zeilen durchgehen
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

for i, line in enumerate(lines):
    url = extract_url(line)
    
    if not url:
        print(f"[!] Zeile {i+1} übersprungen – keine URL erkannt.")
        continue

    url_part = url.rstrip('/').split('/')[-1] or f"seite_{i+1}"
    filename = os.path.join(directory, f"{url_part}.html")

    scrape_and_save(url, filename)

import requests
from bs4 import BeautifulSoup

def scrape_and_save(url, filename):
    try:
        # Webseite abrufen
        response = requests.get(url)
        response.raise_for_status()  # Fehler abfangen
        
        # HTML mit BeautifulSoup parsen
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Nur den sichtbaren Text extrahieren
        text_lines = soup.get_text(separator='\n', strip=True).split('\n')
        
        # Zeilen 48 bis 53 extrahieren
        selected_lines = '\n'.join(text_lines[47:53])
        
        # In Datei speichern
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(selected_lines)
        
        print(f"Inhalt erfolgreich in {filename} gespeichert.")
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Webseite: {e}")

# Beispielaufruf
url = "https://www.spiegel.de/politik/deutschland/"
filename = "F:\Prog\ATD\Projekte\Kris\Output\webseiten_inhalt.txt"
scrape_and_save(url, filename)

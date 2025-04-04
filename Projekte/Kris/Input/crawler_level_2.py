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
        text = soup.get_text(separator='\n', strip=True)
        
        # In Datei speichern
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
        
        print(f"Inhalt erfolgreich in {filename} gespeichert.")
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Webseite: {e}")


        # Durchsucht die Datei crawler_meta.py nach Zeile x
with open("F:\Prog\ATD\Projekte\Kris\Output\crawler_meta_output.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()  # Alle Zeilen in eine Liste einlesen

# Die gewünschte Zeile extrahieren (z. B. dritte Zeile, index 2)
variable = lines[0].strip() if len(lines) > 2 else ""
print(variable)  # Gibt Zeile x aus





url = "https://www.spiegel.de/politik/deutschland/"
filename = "F:\Prog\ATD\Projekte\Kris\Output\l2_output.txt"
scrape_and_save(url, filename)

import requests
from bs4 import BeautifulSoup
import os

# Funktion zum Abrufen und Speichern des Artikels
def scrape_article(url, save_directory):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Sicherstellen, dass die Anfrage erfolgreich war
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Den Artikeltext extrahieren (wir nehmen an, dass der Text in einem <div> mit dem Attribut 'data-area="body"' liegt)
        article_body = soup.find('div', {'data-area': 'body'})
        
        # Falls der Artikeltext gefunden wurde
        if article_body:
            article_text = article_body.get_text(separator='\n', strip=True)
            
            # Den Titel des Artikels als Dateinamen verwenden
            article_title = soup.find('h1').get_text(strip=True)
            article_title = article_title.replace(' ', '_').replace('/', '_').replace('?', '').replace(':', '')  # Ersetze ungültige Zeichen
            
            # Erstelle den Dateipfad
            filename = os.path.join(save_directory, f"{article_title}.txt")
            
            # Speichern des Artikels als Textdatei
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(article_text)
            
            print(f"Artikel gespeichert: {filename}")
        else:
            print(f"Artikeltext nicht gefunden: {url}")
    
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen des Artikels {url}: {e}")

# Beispielaufruf
url = "https://www.spiegel.de/wissenschaft/mensch/donald-trump-helfen-die-zoelle-am-ende-dem-klima-a-d16955a4-1a9c-4745-8c34-e478c6b54656"
save_directory = "F:/Prog/ATD/Projekte/Kris/Output"  # Verzeichnis zum Speichern der Textdateien

# Sicherstellen, dass das Verzeichnis existiert
os.makedirs(save_directory, exist_ok=True)

# Speichern des Artikels
scrape_article(url, save_directory)

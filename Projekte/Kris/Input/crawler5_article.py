import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

# Funktion zum Abrufen und Speichern des Artikels
def scrape_article(url, save_directory):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Sicherstellen, dass die Anfrage erfolgreich war
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Den Artikeltext extrahieren
        article_body = soup.find('div', {'data-area': 'body'})
        
        if article_body:
            article_text = article_body.get_text(separator='\n', strip=True)

            # Aktuelle Zeit einfügen
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            article_text = f"[Erstellt am: {timestamp}]\n\n{article_text}"

            # Titel als Dateiname
            article_title = soup.find('h1').get_text(strip=True)
            article_title = article_title.replace(' ', '_').replace('/', '_').replace('?', '').replace(':', '')
            
            filename = os.path.join(save_directory, f"{article_title}.txt")
            
            # Datei speichern
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(article_text)

            print(f"Artikel gespeichert: {filename}")
        else:
            print(f"Artikeltext nicht gefunden: {url}")
    
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen des Artikels {url}: {e}")

# Funktion zum Abrufen der URLs aus einer Datei
def read_article_links(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

# Hauptcode
article_links_file = "F:/Prog/ATD/Projekte/Kris/Output/txt_links/article_links.txt"
save_directory = "F:/Prog/ATD/Projekte/Kris/Output/article"
os.makedirs(save_directory, exist_ok=True)

article_links = read_article_links(article_links_file)

for idx, url in enumerate(article_links):
    print(f"Verarbeite Artikel {idx + 1}/{len(article_links)}: {url}")
    scrape_article(url, save_directory)

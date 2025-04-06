import requests
from bs4 import BeautifulSoup
import os

# Funktion zum Extrahieren und Speichern der Artikel-Links
def scrape_article_links(base_url, save_directory):
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Sicherstellen, dass die Anfrage erfolgreich war
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Alle Artikel-Links extrahieren (wir suchen nach 'a'-Tags mit der entsprechenden Klasse)
        article_links = soup.find_all('a', class_='text-black dark:text-shade-lightest block')
        
        # Speichern der Links in einer Menge (Set), um Duplikate zu vermeiden
        links = set()  # Ein Set speichert nur eindeutige Links
        
        # Schleife über alle gefundenen Links und Hinzufügen zur Menge
        for link in article_links:
            article_url = link.get('href')
            
            # Stelle sicher, dass der Link eine vollständige URL ist
            if article_url and not article_url.startswith('http'):
                article_url = 'https://www.spiegel.de' + article_url  # Falls der Link relativ ist
            
            links.add(article_url)  # Link zur Menge (Set) hinzufügen
        
        # Speichern der Links in einer Textdatei
        links_file_path = os.path.join(save_directory, 'article_links.txt')
        with open(links_file_path, 'w', encoding='utf-8') as links_file:
            for idx, link in enumerate(links):
                links_file.write(link + '\n')  # Jeden Link in eine neue Zeile
                print(f"[{idx + 1}] Link gespeichert: {link}")
    
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Seite {base_url}: {e}")

# Hauptcode
base_url = "https://www.spiegel.de/wissenschaft/"  # URL der Wissenschafts-Rubrik
save_directory = "F:/Prog/ATD/Projekte/Kris/Output/txt_links"  # Verzeichnis zum Speichern der Textdatei mit Links

os.makedirs(save_directory, exist_ok=True)  # Falls das Verzeichnis noch nicht existiert

# Alle Artikel-Links extrahieren und speichern
scrape_article_links(base_url, save_directory)

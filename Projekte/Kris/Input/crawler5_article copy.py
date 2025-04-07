import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import hashlib  # Für Hash aus der URL

# Funktion zum Abrufen und Speichern des Artikels
def scrape_article(url, article_directory, html_directory):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Titel aus dem Meta-Tag (für Erkennung von Spiegel+ Artikeln)
        meta_title_tag = soup.find('meta', property='og:title')
        is_spiegel_plus = False
        if meta_title_tag and meta_title_tag.get('content', '').startswith('(S+)'):
            is_spiegel_plus = True

        # Titel aus <h1>
        article_title_tag = soup.find('h1')
        article_title = article_title_tag.get_text(strip=True) if article_title_tag else "Unbenannter_Artikel"

        # Ungültige Zeichen entfernen
        invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            article_title = article_title.replace(char, '_')

        # + am Anfang für Spiegel+ Artikel
        if is_spiegel_plus:
            article_title = "+" + article_title

        # Hash aus URL generieren (für eindeutige Benennung)
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:6]
        article_title = f"{article_title}_{url_hash}"

        # Sicherstellen, dass die Dateinamen eindeutig sind
        def get_unique_filename(directory, filename):
            counter = 1
            base_filename, extension = os.path.splitext(filename)
            while os.path.exists(os.path.join(directory, filename)):
                filename = f"{base_filename}_{counter}{extension}"
                counter += 1
            return filename

        # Dateinamen vorbereiten
        html_filename = get_unique_filename(html_directory, f"{article_title}.html")

        # HTML-Rohdaten speichern
        with open(os.path.join(html_directory, html_filename), 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"HTML-Rohdaten gespeichert: {html_filename}")

        # Wenn kein Spiegel+ Artikel: Textdatei zusätzlich speichern
        if not is_spiegel_plus:
            article_body = soup.find('div', {'data-area': 'body'})

            if article_body:
                article_text = article_body.get_text(separator='\n', strip=True)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                article_text = f"[Erstellt am: {timestamp}]\n\n{article_text}"

                text_filename = get_unique_filename(article_directory, f"{article_title}.txt")

                with open(os.path.join(article_directory, text_filename), 'w', encoding='utf-8') as file:
                    file.write(article_text)
                print(f"Artikeltext gespeichert: {text_filename}")
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
base_directory = "F:/Prog/ATD/Projekte/Kris/Output"
article_directory = os.path.join(base_directory, 'article')
html_directory = os.path.join(base_directory, 'html_files')

os.makedirs(article_directory, exist_ok=True)
os.makedirs(html_directory, exist_ok=True)

article_links = read_article_links(article_links_file)

processed_urls = set()  # Verarbeitete URLs merken (zur Sicherheit)

for idx, url in enumerate(article_links):
    # Hash für die URL erzeugen
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:6]

    # Prüfen, ob bereits eine HTML-Datei mit diesem Hash im Dateinamen existiert
    html_exists = any(url_hash in fname for fname in os.listdir(html_directory))

    if html_exists:
        print(f"[{idx + 1}] HTML-Datei bereits vorhanden – überspringe: {url}")
        continue

    print(f"[{idx + 1}] Verarbeite Artikel: {url}")
    scrape_article(url, article_directory, html_directory)


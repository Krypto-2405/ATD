import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

def create_folder(base_dir, title):
    # Erstelle einen Ordner mit Titel, Datum und Uhrzeit
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    safe_title = "_".join(title.split())[:50]  # Titel kürzen und anpassen
    folder_name = f"{safe_title}_{timestamp}"
    folder_path = os.path.join(base_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def download_page(url, folder_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        file_path = os.path.join(folder_path, "index.html")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"Seite heruntergeladen und gespeichert: {url}")
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Herunterladen der Seite: {url} - {e}")

def find_article_links(start_url, base_url):
    try:
        response = requests.get(start_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Finde alle Links zu Artikeln auf der Startseite
        links = []
        for a_tag in soup.find_all("a", href=True):
            href = urljoin(base_url, a_tag['href'])
            if base_url in href and "artikel" in href.lower():  # Bedingung: "artikel" im Link
                links.append(href)

        return list(set(links))  # Entferne doppelte Links
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen der Startseite: {start_url} - {e}")
        return []

def main():
    start_url = "https://www.example.com/startseite"  # Start-URL anpassen
    base_url = "https://www.example.com"  # Basis-URL der Webseite
    base_dir = "heruntergeladene_artikel"  # Basisordner für gespeicherte Artikel
    os.makedirs(base_dir, exist_ok=True)

    article_links = find_article_links(start_url, base_url)

    for link in article_links:
        folder_path = create_folder(base_dir, link.split("/")[-1])  # Ordner basierend auf Linkname
        download_page(link, folder_path)

if __name__ == "__main__":
    main()

from bs4 import BeautifulSoup
import os

# Zielverzeichnis definieren
directory = "F:/Prog/ATD/Projekte/Kris/Output"

# Falls das Verzeichnis nicht existiert, erstellen
os.makedirs(directory, exist_ok=True)

# Dateipfad zur HTML-Datei
file_path = r"F:/Prog/ATD/Projekte/Kris/Output/meta_output.html"

# Dateiname mit vollständigem Pfad setzen
filename = os.path.join(directory, "level_2_output.txt")

# Überprüfen, ob die Datei existiert
if not os.path.exists(file_path):
    print(f"Fehler: Die Datei {file_path} existiert nicht.")
else:
    # HTML-Datei einlesen
    with open(file_path, "r", encoding="utf-8") as file:
        html_data = file.read()

    # HTML parsen
    soup = BeautifulSoup(html_data, "html.parser")

    # <ul>-Element mit der Klasse "polygon-swiper-wrapper" finden
    ul_element = soup.find("ul", class_="polygon-swiper-wrapper")

    # Falls das <ul>-Element existiert, Links extrahieren
    if ul_element:
        links = ul_element.find_all("a")
        
        print("Gefundene Reiter-Links:")
        for link in links:
            print(f"Text: {link.text.strip()}, URL: {link['href']}")
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(f"Text: {link.text.strip()}, URL: {link['href']}\n")
    else:
        print("Kein <ul>-Element mit der Klasse 'polygon-swiper-wrapper' gefunden.")

#!/usr/bin/env python3

import os
import re
import sqlite3
import hashlib
import datetime
from pathlib import Path

from bs4 import BeautifulSoup

############################################
# KONFIGURATION
############################################

# Ordner, in dem alle Artikel-Unterordner liegen:
ARTICLES_DIR = Path("articles")

# (Optionale) Liste von Keywords, nach denen im Artikeltext gesucht werden soll
# In der Praxis ggf. viel umfangreicher oder dynamisch eingelesen
KEYWORDS = [
    "Politik", "Ausland", "Teamwork", "Kreml", "Russland", "Wladimir Putin",
    "Arbeitszeiten", "Urlaubszeiten", "Sergej Iwanow"
]

# Datenbank-Datei
DB_FILE = "articles.sqlite"

############################################
# HILFSFUNKTIONEN
############################################

def init_db(connection):
    """
    Legt die nötigen Tabellen an (falls noch nicht vorhanden).
    """
    cursor = connection.cursor()
    # Beispiel: Eine Tabelle für Artikel-Metadaten
    # - id (PRIMARY KEY)
    # - article_id (eindeutige ID eines Artikels, z. B. basierend auf URL oder Hash)
    # - version_timestamp (wann wurde diese Version gespeichert?)
    # - title
    # - author
    # - publication_date
    # - rubrik
    # - keywords (kommasepariert oder JSON)
    # - content_hash (MD5 oder SHA256, um Änderungen zu vergleichen)
    # - full_html (optional, wenn du den gesamten Inhalt speichern möchtest)

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS article_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article_id TEXT NOT NULL,
            version_timestamp TEXT NOT NULL,
            title TEXT,
            author TEXT,
            publication_date TEXT,
            rubrik TEXT,
            keywords TEXT,
            content_hash TEXT,
            full_html TEXT
        )
        """
    )

    # Beispiel: Tabelle für Auswertungen könnte man auf Basis obiger Tabelle erstellen,
    # oder man macht nur Abfragen/Views darauf.

    connection.commit()


def parse_html_file(html_path):
    """
    Liest eine HTML-Datei ein, extrahiert Meta-Infos:
    - Titel
    - Autor
    - Veröffentlichungsdatum (sofern auffindbar)
    - Rubrik/Unterrubrik
    - Gefundene Keywords im Text
    - Gesamter HTML-Inhalt (optional)
    """
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Beispiel: Titel aus <title> oder <h1> extrahieren
    title_tag = soup.find("title")
    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        title = "Unbekannt"

    # Beispiel: Autor, sofern in <meta name="author" content="..." /> vorhanden
    # (Das muss an die echte Spiegel-HTML angepasst werden)
    author_meta = soup.find("meta", attrs={"name": "author"})
    if author_meta and author_meta.get("content"):
        author = author_meta["content"].strip()
    else:
        # Oder: in <span class="author"> ... </span> etc.
        # Hier nur ein Platzhalter:
        author = "UnknownAuthor"

    # Beispiel: Veröffentlichungsdatum -> Manche Seiten haben <meta property="article:published_time" content="2024-12-28T12:00:00Z" />
    pub_date_meta = soup.find("meta", attrs={"property": "article:published_time"})
    if pub_date_meta and pub_date_meta.get("content"):
        publication_date = pub_date_meta["content"]
    else:
        publication_date = None

    # Rubrik extrahieren -> z. B. in <meta property="article:section" content="Politik" />
    rubrik_meta = soup.find("meta", attrs={"property": "article:section"})
    if rubrik_meta and rubrik_meta.get("content"):
        rubrik = rubrik_meta["content"]
    else:
        rubrik = "UnbekannteRubrik"

    # Keywords suchen -> Im Text (oder in <meta name="keywords">)
    found_keywords = []
    text_content = soup.get_text(separator=" ")
    for kw in KEYWORDS:
        if kw.lower() in text_content.lower():
            found_keywords.append(kw)

    # Optional: HTML-Hash (zur Erkennung von Veränderungen)
    content_hash = hashlib.md5(html_content.encode("utf-8")).hexdigest()

    # Rückgabe der Infos in einem Dictionary
    return {
        "title": title,
        "author": author,
        "publication_date": publication_date,
        "rubrik": rubrik,
        "keywords": found_keywords,
        "content_hash": content_hash,
        "full_html": html_content
    }


def extract_article_id(folder_path):
    """
    Erzeugt eine eindeutige ID für den Artikel.
    Du kannst z. B. den Ordnernamen oder die URL oder einen Hash verwenden.
    Hier nehmen wir einfach den Ordnernamen als "article_id".
    """
    return folder_path.name


def save_to_db(conn, article_id, data):
    """
    Speichert eine neue "Version" eines Artikels in die DB.
    """
    now = datetime.datetime.now().isoformat()
    cursor = conn.cursor()

    # Prüfen, ob wir bereits eine Version mit identischem content_hash haben
    cursor.execute(
        """
        SELECT id FROM article_versions
         WHERE article_id = ? AND content_hash = ?
        """,
        (article_id, data["content_hash"])
    )
    row = cursor.fetchone()
    if row:
        # Diese Version existiert schon -> nicht nochmal speichern
        print(f"Artikel {article_id} - identische Version bereits in DB.")
        return

    # Neue Version einfügen
    cursor.execute(
        """
        INSERT INTO article_versions (
            article_id,
            version_timestamp,
            title,
            author,
            publication_date,
            rubrik,
            keywords,
            content_hash,
            full_html
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            article_id,
            now,
            data["title"],
            data["author"],
            data["publication_date"],
            data["rubrik"],
            ",".join(data["keywords"]),  # evtl. JSON ablegen
            data["content_hash"],
            data["full_html"]
        )
    )
    conn.commit()
    print(f"Artikel {article_id} - neue Version gespeichert.")


############################################
# HAUPTFUNKTION
############################################

def main():
    # 1) DB-Verbindung aufbauen
    conn = sqlite3.connect(DB_FILE)
    init_db(conn)

    # 2) Alle Unterordner im ARTICLES_DIR durchgehen
    #    und dort index.html oder *.html-Dateien suchen
    if not ARTICLES_DIR.exists():
        print("Fehler: ARTICLES_DIR existiert nicht.")
        return

    for folder in ARTICLES_DIR.iterdir():
        if folder.is_dir():
            # Erwartet: In jedem Unterordner liegt mind. eine HTML-Datei (z. B. index.html)
            html_files = list(folder.glob("*.html"))
            if not html_files:
                continue

            article_id = extract_article_id(folder)

            for html_file in html_files:
                data = parse_html_file(html_file)
                save_to_db(conn, article_id, data)

    # 3) Kurze Auswertung: Anzahl Artikel pro Veröffentlichungs-Wochentag
    print("\n--- Auswertung: Anzahl Artikel pro Wochentag ---")
    cursor = conn.cursor()
    # publication_date sollte ein ISO-Datum oder -Datum+Uhrzeit sein.
    # Man kann in SQLite eine Funktion strftime() nutzen, um den Wochentag zu extrahieren.
    # ABER: Nur wenn wir "richtige" Datum-/Zeitformate haben.
    # Angenommen, publication_date ist im Format '2024-12-28T12:00:00Z',
    # dann müssen wir das ggf. umbauen.

    # Einfaches Beispiel: wir ignorieren die Zeitzone und versuchen:
    cursor.execute("""
        SELECT publication_date
        FROM article_versions
        WHERE publication_date IS NOT NULL
    """)
    counts = {}
    for (pub_date_str,) in cursor.fetchall():
        # pub_date_str = "2024-12-28T12:00:00Z"
        # extrahiere "2024-12-28" -> Wochentag
        date_part = pub_date_str.split("T")[0]  # "2024-12-28"
        try:
            dt_obj = datetime.datetime.strptime(date_part, "%Y-%m-%d")
            weekday_name = dt_obj.strftime("%A")  # z. B. "Saturday"
            counts[weekday_name] = counts.get(weekday_name, 0) + 1
        except ValueError:
            # Datum nicht parsebar
            continue

    for wday, cnt in counts.items():
        print(f"{wday}: {cnt} Artikel")

    # Beispiel: Ausgabe der Anzahl Artikel nach Rubrik
    print("\n--- Auswertung: Anzahl Artikel pro Rubrik ---")
    cursor.execute("""
        SELECT rubrik, COUNT(*) as cnt
        FROM article_versions
        GROUP BY rubrik
        ORDER BY cnt DESC
    """)
    for row in cursor.fetchall():
        print(f"Rubrik '{row[0]}': {row[1]} Artikel")

    conn.close()


if __name__ == "__main__":
    main()

import subprocess
import os

directory = "F:/Prog/ATD/Projekte/Kris/Input"

# Liste der Skripte, die du ausführen möchtest
scripts = [
    "crawler1_meta.py",
    "crawler2_txt.py",
    "crawler3_html_write.py",
    "crawler4_article_links.py",
    "crawler5_article.py",

]

# Alle Skripte nacheinander ausführen
for script in scripts:
    subprocess.run(["python", script])
    print(f"{script} wurde ausgeführt.")

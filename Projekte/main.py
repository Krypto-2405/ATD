import requests
from bs4 import BeautifulSoup

URL = 'https://www.spiegel.de/politik/deutschland/frontex-chef-hans-leijtens-ein-zaun-allein-ist-noch-keine-loesung-a-9a3c9789-ab8c-4aa5-aedc-a1ee80e91e34' ## https://www.spiegel.de/politik/deutschland/
website = requests.get(URL)
results = BeautifulSoup(website.content, 'html.parser')

blogbeitraege = results.find_all('div', class_='awr')

for blogbeitrag in blogbeitraege: 
    blog_titel = blogbeitrag.find('h2', class_='entry-title')
    print(blog_titel.text)
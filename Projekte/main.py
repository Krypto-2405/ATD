import requests
from bs4 import BeautifulSoup

URL = 'https://google.com'
website = requests.get(URL)
results = BeautifulSoup(website.content, 'html.parser')

blogbeitraege = results.find_all('div', class_='awr')

for blogbeitrag in blogbeitraege: 
    blog_titel = blogbeitrag.find('h2', class_='entry-title')
    print(blog_titel)
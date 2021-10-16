import bs4
import requests
from pprint import pprint
import re


FAVORITE_HUBS = {'дизайн', 'фото', 'web', 'python'}
re_hubs = re.compile('[' + '|'.join(FAVORITE_HUBS) + ']',re.IGNORECASE)
response = requests.get('https://habr.com/ru/all')
response.raise_for_status()
soup = bs4.BeautifulSoup(response.text, features='html.parser')
articles = soup.find_all('article')
for article in articles:
    datetime = article.find(class_='tm-article-snippet__datetime-published').text
    author = article.find(class_='tm-user-info__username').text.strip()
    title = article.find('h2').text.strip()
    href = article.find(class_='tm-article-snippet__title-link').attrs['href']
    link = 'https://habr.com' + href
    hubs = article.find_all(class_='tm-article-snippet__hubs-item')
    hubs = set(hub.find('span').text for hub in hubs)
    if FAVORITE_HUBS & hubs:
         print(f'Found in hubs: {datetime} {title} {link}')
    else:
        response_t = requests.get(link)
        response_t.raise_for_status()
        soup_t = bs4.BeautifulSoup(response_t.text, features='html.parser')
        soup_tf = []
        soup_tf = soup_t.find_all(re_hubs)
        if soup_tf:
            print(f'Found in text: {datetime} {title} {link}')

#

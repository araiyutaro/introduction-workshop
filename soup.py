import requests
from bs4 import BeautifulSoup

url_suntory = "https://www.suntory.co.jp/"
url_kirin = "https://www.kirin.co.jp/"

res = requests.get(url_kirin)

soup = BeautifulSoup(res.content, "html.parser")
# title タグの文字列を取得する
title_text = soup.find('title').get_text()
print(title_text)
# > Quotes to Scrape

# ページに含まれるリンクを全て取得する
links = [url.get('href') for url in soup.find_all('a')]
print(links)
print(len(links))

# class が quote の div 要素を全て取得する
quote_elms = soup.find_all('div', {'class': 'quote'})
print(len(quote_elms))

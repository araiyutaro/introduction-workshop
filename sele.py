import urllib.parse
from urllib.parse import urlparse

import spacy
from publicsuffix2 import get_sld
from selenium import webdriver
from selenium.webdriver.common.by import By

url_suntory = "https://www.suntory.co.jp/"
url_kirin = "https://www.kirin.co.jp/"


def is_same_domain(domain="", link=""):
    return domain in link


def get_same_domain_links(url=""):
    """URLを入力すると、そこに存在するaタグから全てのリンク先を取得し、同一ドメインのリンクのリストを返す。
    リンクからはクエリやフラグメントは取り除かれる。

    :param url: リンク先を取得したいウェブサイトのURL
    :type url: str
    :return: リンク先リスト
    :rtype: list[str]
    """
    domain = get_sld(urlparse(url).netloc)

    driver = webdriver.Chrome()
    driver.get(url)
    a_elements = driver.find_elements(By.TAG_NAME, 'a')
    links = []
    for element in a_elements:
        u = urllib.parse.urlparse(element.get_attribute('href'))
        links.append(u.scheme + "://" + u.netloc + u.path)
    links = set(links)
    links = list(filter(lambda x: is_same_domain(domain, x), links))
    links = list(filter(lambda x: x != url, links))
    links = set(links)
    driver.quit()
    print("same_domain_links:")
    print(links)
    print("リンク先の数：" + str(len(links)))
    return links


def get_website_word_list(url=""):
    """URLを入力すると、そのウェブサイトに記載されているinner-textから普通名詞を抽出してリストに返す

    :param url: 単語を取得したいウェブサイトのURL
    :type url: str
    :return: 単語リスト
    :rtype: list[str]
    """
    driver = webdriver.Chrome()
    driver.get(url)
    body_element = driver.find_element(By.TAG_NAME, "body")
    body_text = body_element.text

    nlp = spacy.load("ja_ginza")
    chunk_size = 10000
    words_list = []
    for i in range(0, len(body_text), chunk_size):
        chunk = body_text[i:i + chunk_size]
        doc = nlp(chunk)
        for token in doc:
            if token.tag_ in ["名詞-普通名詞-一般"]:
                words_list.append(token.lemma_)
    driver.quit()
    print("website_word_list:")
    print(url)
    print(words_list)
    print("単語数：" + str(len(words_list)))
    return words_list


def get_all_words_list(url=""):
    links = get_same_domain_links(url)
    words = get_website_word_list(url)
    for link in links:
        words = words + get_website_word_list(link)
    return words


# links_suntory = get_same_domain_links(url_suntory)
# links_kirin = get_same_domain_links(url_kirin)
# print(links_suntory)
# print(len(links_suntory))
# print(links_kirin)
# print(len(links_kirin))
# words_suntory = get_website_word_list(url_suntory)
# words_kirin = get_website_word_list(url_kirin)
# print(words_suntory)
# print(len(words_suntory))
# print(words_kirin)
# print(len(words_kirin))
all_words_suntory = get_all_words_list(url_suntory)
print("all_words:")
print(all_words_suntory)
print("全単語数" + str(len(all_words_suntory)))
all_words_set = set(all_words_suntory)
result = []
for word in all_words_set:
    word_count = all_words_suntory.count(word)
    result.append((word, word_count))
result.sort(key=lambda x: x[1], reverse=True)
print("〜〜〜全単語とその頻度〜〜〜")
print(result)

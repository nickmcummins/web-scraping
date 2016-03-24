import sys
from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup

BASE_URL = "http://molecularautism.biomedcentral.com"
OUTPUT_DIR = "/home/nick/Articles/Molecular-Autism"

article_url = sys.argv[1]


def download_file(url, title):
    response = urlopen(url)
    with open(generate_file_name(title, 'pdf'), 'wb') as file:
        file.write(response.read())


def generate_file_name(title, extension):
    return OUTPUT_DIR + "/" + title.replace(' ', '-').lower() + "." + extension


def generate_html_article_url(article_url_main):
    return article_url_main


def download_html(url, title):
    article_html = urlopen(url)
    with open(generate_file_name(title, 'html'), 'w') as file:
        html_bs_obj = BeautifulSoup(article_html.read(), "lxml")
        article_main_bs_obj = html_bs_obj.find("div", {"class": "Main_content"})
        file.write(article_main_bs_obj.decode_contents(formatter="html"))

try:
    html = urlopen(article_url)
except HTTPError as e:
    print(e)
else:
    bs_obj = BeautifulSoup(html.read(), "lxml")
    article_title = bs_obj.find("h1", {"class": "ArticleTitle"}).get_text()
    pdf_link = BASE_URL + bs_obj.find("a", {"id": "articlePdf"})['href']
    print(article_title)
    print(pdf_link)
    download_file(pdf_link, article_title)
    html_link = generate_html_article_url(article_url)
    print(html_link)
    download_html(html_link, article_title)

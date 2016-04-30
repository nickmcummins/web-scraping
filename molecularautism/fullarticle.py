from urllib.error import HTTPError
from urllib.request import urlopen

from bs4 import BeautifulSoup
import re

BASE_URL = "http://molecularautism.biomedcentral.com"
OUTPUT_DIR = "/home/nick/Articles/Molecular-Autism"


class FullArticle:
    def __init__(self, url):
        self.url = url

        try:
            html = urlopen(url)
        except HTTPError as e:
            print(e)
        else:
            bs_obj = BeautifulSoup(html.read(), "lxml")
            self.title = bs_obj.find("h1", {"class": "ArticleTitle"}).get_text()
            self.pdfUrl = BASE_URL + bs_obj.find("a", {"id": "articlePdf"})['href']
            # print(article_title)
            # print(pdf_link)
            # download_file(pdf_link, article_title)
            self.htmlUrl = url
            # print(html_link)
            # download_html(html_link, article_title)

    def download_pdf(self):
        response = urlopen(self.pdfUrl)
        with open(self.generate_file_name('pdf'), 'wb') as file:
            file.write(response.read())

    def generate_file_name(self, extension):
        nonalphanumeric = re.compile('\W')
        filename = OUTPUT_DIR + "/"
        filename += re.sub(nonalphanumeric, '', self.title.replace(' ', '-'))
        filename += extension.lower()
        return filename

    def download_html(self):
        article_html = urlopen(self.url)
        with open(self.generate_file_name('html'), 'w') as file:
            html_bs_obj = BeautifulSoup(article_html.read(), "lxml")
            article_main_bs_obj = html_bs_obj.find("div", {"class": "Main_content"})
            file.write(article_main_bs_obj.decode_contents(formatter="html"))

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
            self.htmlUrl = url

    def download_pdf(self):
        response = urlopen(self.pdfUrl)
        filename = self.generate_file_name('pdf')
        with open(filename, 'wb') as file:
            file.write(response.read())
        print("\t\tDownloaded PDF " + self.url + " to " + filename)

    def generate_file_name(self, extension):
        nonalphanumericdash = re.compile('[^a-zA-Z0-9_-]')
        filename = OUTPUT_DIR + "/"
        filename += re.sub(nonalphanumericdash, '', self.title.replace(' ', '-'))
        filename += '.' + extension
        return filename

    def download_html(self):
        article_html = urlopen(self.url)
        filename = self.generate_file_name('html')
        with open(filename, 'w') as file:
            html_bs_obj = BeautifulSoup(article_html.read(), "lxml")
            article_main_bs_obj = html_bs_obj.find("div", {"class": "Main_content"})
            file.write(article_main_bs_obj.decode_contents(formatter="html"))
        print("\t\tDownloaded HTML " + self.url + " to " + filename)

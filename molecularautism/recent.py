import yaml
from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.request import urlopen

from molecularautism.article import Article

YAML_STORE = "/home/nick/Articles/Molecular-Autism/Articles.yaml"
MOLECULAR_AUTISM_HOME = "http://molecularautism.biomedcentral.com"


class MolecularAutismRecent:

    def __init__(self):
        self.downloadedArticles = self.load_yaml_store()
        self.recentArticles = self.check_recent_from_web()

    @staticmethod
    def load_yaml_store():
        with open(YAML_STORE, 'r') as file:
            articles_list = yaml.load(file)
        return articles_list

    @staticmethod
    def check_recent_from_web():
        try:
            page_html = urlopen(MOLECULAR_AUTISM_HOME)
        except HTTPError as e:
            print(e)
        else:
            bs_obj = BeautifulSoup(page_html.read(), "lxml")
            recent_articles = bs_obj.find("div", {"id": "recent-articles"}).findAll("a", {"class": "fulltexttitle"})
            return list(map(Article.from_html, recent_articles))

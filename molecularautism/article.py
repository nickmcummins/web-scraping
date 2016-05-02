from .fullarticle import FullArticle

MOLECULAR_AUTISM_HOME = "http://molecularautism.biomedcentral.com"


class Article:
    def __init__(self, a):
        self.title = a.get_text()
        self.url = self.generate_url(a['href'])
        self.id = self.parse_id(a['href'])

    def __repr__(self):
        return self.url

    @staticmethod
    def generate_url(relative_url):
        return MOLECULAR_AUTISM_HOME + relative_url

    @staticmethod
    def parse_id(relative_url):
        return relative_url.split("/")[2] + "/" + relative_url.split("/")[3]

    @staticmethod
    def from_html(article):
        return Article(article)

    def to_full_article(self):
        return FullArticle(self.url)

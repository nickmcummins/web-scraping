from molecularautism.fullarticle import FullArticle
from molecularautism.recent import MolecularAutismRecent

latestArticles = MolecularAutismRecent()

for article in latestArticles.recentArticles:
    fullArticle = FullArticle(article.url)
    fullArticle.download_pdf()
    fullArticle.download_html()

import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup 

url = sys.argv[1] 
html = urlopen(url)
bsObj = BeautifulSoup(html.read(), "lxml") 

articleTitle = bsObj.find("h1", {"class": "ArticleTitle"})
abstract = bsObj.find("section", {"class": "Abstract"}).div.p


print(articleTitle.get_text()) 
print("\n")
print("<p><a href='%s' target='blank'>View article full on <em>Molecular Autism</em></a></p>" % (url))
print("\n")
print("<p>%s</p>" % (abstract.get_text()))




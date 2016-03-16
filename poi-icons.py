import sys, wget
from urllib.request import urlopen 
from bs4 import BeautifulSoup 



html = urlopen("http://www.poi-factory.com/gps-icons") 
bsObj = BeautifulSoup(html.read(), "lxml") 

icons = bsObj.find("div", {"class": "content"}).findAll("li") 

def icon_file_name(node): 
    return node.get_text().replace(" BMP Icon", "").replace(" ", "-").lower()
    
def icon_image_url(node): 
    iconPageUrl = node.find("a")['href']            
    iconPage = urlopen("http://www.poi-factory.com" + iconPageUrl) 
    iconBsObj = BeautifulSoup(iconPage.read(), "lxml") 
    imageDiv = iconBsObj.find("div", {"class": "node_images"})
    if imageDiv is not None: 
        iconUrl = imageDiv.img['src'] 
        wget.download(iconUrl) 
    

for icon in icons: 
    icon_image_url(icon) 

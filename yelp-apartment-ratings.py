from urllib.parse import urlencode
from urllib.request import urlopen

from bs4 import BeautifulSoup


def write_to_file(business_name, business_rating):
    with open("apartment-ratings.tsv", 'a') as output_file:
        output_file.write(business_name + "\t" + business_rating + "\n")


def fetch_business_info(name):
    apartment_search = urlencode({'find_desc': name})
    url = 'https://www.yelp.com/search?find_loc=Seattle%2C+WA&ns=1&'
    url_query = url + apartment_search
    print(url_query)
    html = urlopen(url_query)
    bs_obj = BeautifulSoup(html.read(), "lxml")
    business_result = bs_obj.find("li", {"class": "regular-search-result"})
    if business_result is None:
        business_name = name
        business_rating_obj = None
        business_rating_count_obj = None
    else:
        business_name = business_result.find("a", {"class": "biz-name"}).get_text()
        business_rating_obj = business_result.find("i", {"class": "star-img"})
        business_rating_count_obj = business_result.find("span", {"class": "review-count"})

    if business_rating_obj is not None and business_rating_count_obj is not None:
        business_rating = business_rating_obj['title'].replace(' star rating', '')
        business_rating_count = business_rating_count_obj.get_text().strip().replace('reviews', '').replace('review',
                                                                                                            '')
        write_to_file(business_name, business_rating + ' ' + business_rating_count)
    else:
        write_to_file(business_name, '')


def sanitize_building_name(name):
    return name.replace('Pre-sign', '').replace('Pre-Sign', '')


with open("waveg-buildings.gps") as f:
    buildings = f.readlines()

for building in buildings:
    building_name = building.split("\t")[0]
    fetch_business_info(sanitize_building_name(building_name))

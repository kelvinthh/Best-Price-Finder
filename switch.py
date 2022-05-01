from bs4 import BeautifulSoup
from tqdm import tqdm
import requests

def findSwitch(pageNo):
    url = "https://www.price.com.hk/search.php?g=E&header_type=E&q=Switch&page=" + str(pageNo)
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    items = soup.find_all("div", {"class": "ec-list-product-wrapper"})
    try:
        for item in items:
            delTag = item.find("del")
            spanTags = delTag.find_all("span", {"class": "text-price-number"})
            title = item.img["title"]
            price = 0

            for spanTag in spanTags:
                    price = int(spanTag.string.replace(",", ""))


            if "Switch" in title and "OLED" in title and price > 1000:
                print("--------------------------------")
                print(title)
                print("Price: $" + spanTag.string)
                print("Page " + str(pageNo))
        
    except Exception as e: 
        pass

for i in tqdm(range(1,334)):
    findSwitch(i)
print("Search finished!!!")
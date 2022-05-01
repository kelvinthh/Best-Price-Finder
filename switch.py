from pickletools import TAKEN_FROM_ARGUMENT1
from tkinter import E
from bs4 import BeautifulSoup
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

            if "Switch" in title and "LED" in title:
                print("--------------------------------")
                print(title)
            else:
                continue

            for spanTag in spanTags:
                print("Price: $" + spanTag.string)

            print("Page " + str(pageNo))
                
    except Exception as e: 
        pass

for i in range(1,334):
    findSwitch(i)
print("Search finished!!!")
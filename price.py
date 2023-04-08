import threading
from time import sleep
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import datetime
import os
import re

results = []
search_item = input("Please enter the product name to search >>> ")
price_filter = input("Please enter the minimum price for filtering (HKD) >>> ")

# Get search result max page number
def get_max_page(item):
    url = f"https://www.price.com.hk/search.php?g=E&header_type=E&q={item}&page=1"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination_total = soup.find(class_="pagination-total").span.string.strip()
    max_page = int(re.findall(r'\d+', pagination_total)[0])
    return max_page

# Turns links displayed in terminal clickable
def hyperlink(uri, label=None):
    if label is None: 
        label = uri
    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'
    return escape_mask.format('', uri, label)

# Search for items within a single page
def search(item_name, page):
    url = f"https://www.price.com.hk/search.php?g=E&header_type=E&q={item_name}&page={page}"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    items = soup.find_all("div", {"class": "ec-list-product-wrapper"})

    for item in items:
        price_div = item.find("div", {"class": "ec-product-price"})
        remark_label = price_div.find("span", {"class": "remark-label"})
        if remark_label and "已售罄" in remark_label:
            continue

        price_span = price_div.find("span", {"class": "text-price-number"})
        title = item.img["title"]
        link = item.find("a")["href"]

        if "shop.price.com" not in link:
            link = "https://price.com.hk/" + link

        price = int(price_span.string.replace(",", ""))

        if item_name in title and price > int(price_filter):
            results.append({'price': price, 'title': title, 'link': link})        

max_page = get_max_page(search_item)
threads = []
for i in tqdm(range(1, max_page + 1), "Initizialing"):
    t = threading.Thread(target=search, args=(search_item, i,))
    threads.append(t)
    t.start()
    sleep(0.05)

for x in tqdm(threads, f"Search Completion"):
    x.join()

print("============================================")

sorted_list = sorted(results, key=lambda i: i['price'], reverse=True)
for result in sorted_list:
    print(hyperlink(result.get('link'), f"HK${str(result.get('price'))}   {result.get('title')}"))

    today = datetime.datetime.now()
    date_time = today.strftime("%d-%m-%Y %H-%M-%S")

    directory = "results"
    path = f"./{directory}/Result {date_time}.txt"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, 'a') as f:
        f.write(f"\nHK${str(result.get('price'))} {result.get('title')} {result.get('link')}")

print("====================================================================")
print(f"✅  Search finished, searched {max_page} page(s) and found {len(results)} result(s)")
print(f"🗂  Search result saved to {path}")

import threading
from time import sleep
from tokenize import String
from bs4 import BeautifulSoup
from tqdm import tqdm
from IPython.display import display
import pandas as pd
import requests, datetime, os

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 9000)

results = []
searchItem = input("Please enter the product name to search >>> ")
priceFilter = input("Please enter the minimum price for filtering (HKD) >>> ")

# Get search result max page number
def getMaxPage(item: String) -> int:
    url = f"https://www.price.com.hk/search.php?g=E&header_type=E&q={item}&page=1"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    return int(soup.find(class_="pagination-total").span.string.replace("共 ","").replace(" 頁", ""))

# Turns links displayed in terminal clickable
def hyperlink(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''
    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'
    return escape_mask.format(parameters, uri, label)

# Search for items within a single page
def search(itemName: String, page: int):
    url = f"https://www.price.com.hk/search.php?g=E&header_type=E&q={itemName}&page=" + str(page)
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    items = soup.find_all("div", {"class": "ec-list-product-wrapper"})

    try:
        for item in items:
            priceDiv = item.find("div", {"class": "ec-product-price"})
            remarkLabel = priceDiv.find("span", {"class": "remark-label"})
            if remarkLabel and "已售罄" in remarkLabel:
                continue

            priceSpan = priceDiv.find("span", {"class": "text-price-number"})
        
            title = item.img["title"]
            price = 0
            a_href = item.find("a")["href"]


            if "shop.price.com" in a_href:
                link = a_href
            else:
                link = "https://price.com.hk/"+item.find("a")["href"]

            price = int(priceSpan.string.replace(",", ""))


            if itemName in title and price > int(priceFilter):
                results.append({'price': price, 'title': title, 'link': link})        
    except Exception as e: 
        pass

maxPage = getMaxPage(searchItem)
threads = []
for i in tqdm(range(1,maxPage+1)):
    t = threading.Thread(target=search, args=(searchItem,i,))
    threads.append(t)
    t.start()
    sleep(0.05)


for x in threads:
    x.join()

print("============================================")

sortedList = sorted(results, key = lambda i: i['price'], reverse=True)
for result in sortedList:

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
print(f"✅  Search finished, searched {maxPage} page(s) and found {len(results)} result(s)")
print(f"🗂  Search result saved to {path}")
# df = pd.DataFrame(sortedList)
# display(df)
# with open("df.txt", 'a') as f:
#         f.write(df.to_string())
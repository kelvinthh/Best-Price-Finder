from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import pprint

searchItem = input("Please enter what to search here >>> ")
priceFilter = input("Please enter price no. it should be greater than  >>> ")
url = f"https://www.price.com.hk/search.php?g=E&header_type=E&q={searchItem}&page=1"
result = requests.get(url)
soup = BeautifulSoup(result.text, "html.parser")
maxPageNo = int(soup.find(class_="pagination-total").span.string.replace("共 ","").replace(" 頁", ""))

def hyperlink(uri, label=None):
    if label is None: 
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)

results = []
for i in tqdm(range(1,maxPageNo+1)):
    url = f"https://www.price.com.hk/search.php?g=E&header_type=E&q={searchItem}&page=" + str(i)
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    items = soup.find_all("div", {"class": "ec-list-product-wrapper"})

    try:
        for item in items:
            # delTag = item.find("del")
            # spanTags = delTag.find_all("span", {"class": "text-price-number"})
            # print("JSSDADSA " + item.find_all("div", class_ = "ec-product-price"))
            priceDiv = item.find("div", {"class": "ec-product-price"})
            priceSpan = priceDiv.find("span", {"class": "text-price-number"})
        
            haha = item
            title = item.img["title"]
            price = 0
            a_href = item.find("a")["href"]
            if "shop.price.com" in a_href:
                link = a_href
            else:
                link = "https://price.com.hk/"+item.find("a")["href"]

            price = int(priceSpan.string.replace(",", ""))


            if searchItem in title and price > int(priceFilter):
                # print(f"{title} at Page {i}")
                # print(f"Price: ${spanTag.string}")
                # print(f"Detail: {link}")
                # print("--------------------------------")
                results.append({'title': title, 'price': price, 'link': link})

        
    except Exception as e: 
        pass

print("============================================")
print(f"Search finished, searched {maxPageNo} pages and found {len(results)} result(s)")

# for result in results:
#     # print(f"${str(result.get('price'))}     {result.get('title')}")
#     # print(hyperlink(result.get('link'), 'Click here!~'))
#     print(hyperlink(result.get('link'), f"HK${str(result.get('price'))}   {result.get('title')}"))

sortedList = sorted(results, key = lambda i: i['price'], reverse=True)
for result in sortedList:
    # print(f"${str(result.get('price'))}     {result.get('title')}")
    # print(hyperlink(result.get('link'), 'Click here!~'))
    print(hyperlink(result.get('link'), f"HK${str(result.get('price'))}   {result.get('title')}"))

import requests
import csv
from bs4 import BeautifulSoup

# get prorduct price
def get_price(soup):
    try:
        price = soup.find('span', attrs={'id': 'priceblock_ourprice'}).string.strip()
    except AttributeError:
        try:
            # If there is some deal price
            price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).string.strip()

        except:
            price = "none"

    return price

# get stock
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"

    return available

if __name__ == '__main__':

    headers = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US'})
    url_array = []  # array for urls
    with open('asins.csv', 'r') as csvfile:
        asin_reader = csv.reader(csvfile)
        for row in asin_reader:
            url_array.append(row[0])  # This url list is an array containing all
            # the urls from the excel sheet
    filename = "product-info.csv"
    f = open(filename, 'w')
    csv_headers = "Asin, Price, Stock\n"
    f.write(csv_headers)
    i = 0
    for asin in url_array:
        item_array = []  # An array to store details of a single product.
        amazon_url = "https://www.amazon.com/dp/" + asin  # The general
        webpage = requests.get(amazon_url, headers=headers)
        # Soup Object containing all data
        new_soup = BeautifulSoup(webpage.content, "lxml")
        #price_data = new_soup.find('span', attrs={'id': 'priceblock_ourprice'})
        i+=1
        print(i)
        print(asin)
        print(get_price(new_soup))
        print(get_availability(new_soup))
        f.write(asin + ',' + get_price(new_soup) + ',' + get_availability(new_soup) + '\n')
    f.close()

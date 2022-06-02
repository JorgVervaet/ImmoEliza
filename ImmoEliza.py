from lxml import etree
from bs4 import BeautifulSoup
import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}


url = "https://www.immoweb.be/en/classified/apartment/for-sale/gavere/9890/9937664?searchId=629759872b9e9"
immosite = requests.get(url, headers=headers)
print(url, immosite.status_code)
soup = BeautifulSoup(immosite.content, 'html.parser')
zipc = re.findall("([/]+[\d{4}]+[/])", url)
zipcode = zipc[0].replace("/", "")
print(zipcode)
tables = soup.find_all("tbody")
headings = []
values = []
SPrice = []

gen_table = tables[0].find_all("tr")
int_table = tables[1].find_all("tr")
ext_table = tables[2].find_all("tr")


for row in gen_table:
    for th in row.find_all("th"):
        headings.append(f'{th.contents[0].strip()}')
    for td in row.find_all("td"):
        values.append(f"{td.contents[0].strip()}")

for row in int_table:
    for th in row.find_all("th"):
        headings.append(f'{th.contents[0].strip()}')
    for td in row.find_all("td"):
        values.append(f"{td.contents[0].strip()}")

for row in ext_table:
    for th in row.find_all("th"):
        headings.append(f'{th.contents[0].strip()}')
    for td in row.find_all("td"):
        values.append(f"{td.contents[0].strip()}")

for elem in soup.find_all("p", attrs=("classified__price")):
    price = elem.text
    SPrice = (f"{price.split()[0]}")

dictionary = dict(zip(headings, values))
dictionary["price"] = SPrice
dictionary["zipcode"] = zipcode

print(dictionary)

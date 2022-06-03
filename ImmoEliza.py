from lxml import etree
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

headings = []
values = []
SPrice = []
CompleteDictionary = []

file = open('/Users/Jorg/BeCode/ImmoEliza/data/Links.txt', 'r')
Lines = file.readlines()
#print(Lines)
#immosite = requests.get(Lines, headers=headers)
#print(immosite)

for line in Lines:
    #driver.get(line)
    #soup = BeautifulSoup(driver.page_source)
    #print(Lines.status_code)
    page = requests.get(line)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all("tbody")
    
    zipc = re.findall("([/]+[\d{4}]+[/])", line) #get the zipcode from url
    zipcode = zipc[0].replace("/", "")
    

    gen_table = tables[0].find_all("tr") #collecting general information   
    int_table = tables[1].find_all("tr") 
    ext_table = tables[2].find_all("tr")


    for row in gen_table:
        for th in row.find_all("th"):
            headings.append(f'{th.contents[0].strip()}') #getting all the headings from the page about general info
        for td in row.find_all("td"):
            values.append(f"{td.contents[0].strip()}") #getting all the values from the page about general info

    for row in int_table:
        for th in row.find_all("th"):
            headings.append(f'{th.contents[0].strip()}') #getting all the headings from the page about interior
        for td in row.find_all("td"):
            values.append(f"{td.contents[0].strip()}") #getting all the values from the page about interior

    for row in ext_table:
        for th in row.find_all("th"): #getting all the headings from the page about exterior
            headings.append(f'{th.contents[0].strip()}')
        for td in row.find_all("td"): #getting all the values from the page about exterior
            values.append(f"{td.contents[0].strip()}")

    for elem in soup.find_all("p", attrs=("classified__price")): #getting the price from the page
        price = elem.text
        SPrice = (f"{price.split()[0]}")

    dictionary = dict(zip(headings, values)) #fusing headings and values together
    dictionary["price"] = SPrice #adding the price to the dictionary
    dictionary["zipcode"] = zipcode #adding the zipcode to the dictionary
    print(dictionary)
    CompleteDictionary.append(dictionary)
dfCompleteDictionary = pd.json_normalize(CompleteDictionary)

print(dfCompleteDictionary)
dfCompleteDictionary.to_csv(index=False)
dfCompleteDictionary.to_csv(r'/Users/Jorg/BeCode/ImmoEliza/data/TheDictionary.csv', index=False)


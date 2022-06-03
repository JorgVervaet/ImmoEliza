from lxml import etree
from bs4 import BeautifulSoup
import requests
import re
import selenium

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()



headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

options.add_argument('--start-maximized')
options.add_argument('--disable-infobars')
ser = Service("/Users/Jorg/Drivers/chromedriver") 
driver = webdriver.Chrome(options=options,service=ser)
driver.implicitly_wait(3)


urls = []
for page in range(0, 333):
    p = f"https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&page={page}&orderBy=relevance"
    driver.get(p)
    soup = BeautifulSoup(driver.page_source)
    print(page)
    for link in soup.find_all("a", attrs={"class":"card__title-link"}):
        urls.append(link.get('href'))
        print(link.get('href'))


driver.close()

with open(r'/Users/Jorg/BeCode/ImmoEliza/data/Links.txt', 'w') as fp:
    fp.write('\n'.join(urls))   
    
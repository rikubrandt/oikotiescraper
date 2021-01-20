from os import getenv
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By
import json
import time
from dotenv import load_dotenv
import os
# Only houses from Helsinki
baseURL = "https://asunnot.oikotie.fi/myytavat-uudisasunnot?pagination=1&locations=%5B%5B65,6,%22Vantaa%22%5D%5D&cardType=200"

load_dotenv()
DRIVER_PATH = os.environ.get("DRIVER_PATH")


browser = webdriver.Chrome(DRIVER_PATH)


def firstHouse():
    browser.get(baseURL)
    htmlSource = browser.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')
    firstLink = soup.find('a', attrs={'class': 'ot-card'})['href']
    return firstLink

def findURL(soup):
    return soup.find('a', attrs={'analytics-click-label': 'next'})['href']

def getInfo(soup):
    values = soup.findAll('dd', attrs={'class': 'details-grid__item-value'})
    ##Hinta, vastike, neliöt, huonekpl, kerros, rakennusvuosi, Rak.Tyyppi, Kaupunginosa, Kaupunki
    valueList = []
    for dd in values:
        input = dd.text
        valueList.append(input.encode("ascii", "ignore").decode())
    return valueList


def scraper():
    houses = {}
    firstLink = firstHouse()
    browser.get(firstLink)
    htmlSource = browser.page_source
    soup = BeautifulSoup(htmlSource, 'html.parser')
    numberOfHouses = soup.find('span', attrs={'class': 'button button--navigation button--small button--navigation-muted ng-binding ng-scope'}).text
    ## "1 / 2000"
    pages = int(numberOfHouses[4:])
    
    partUrl = firstLink.split("/")
    id = partUrl[len(partUrl)-1]
    print(id)
    
    getInfo(soup)

    print(houses[id])
    browser.get(findURL(soup))
    for i in range(0, pages-1):
        try:
            element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='button button--navigation button--small ng-scope']")))
            htmlSource = browser.page_source
            soup = BeautifulSoup(htmlSource, 'html.parser')

            partUrl = nextURL.split("/")
            id = partUrl[len(partUrl)-1]
            values = soup.findAll(
                'dd', attrs={'class': 'details-grid__item-value'})
            valueList = []
            for dd in values:
                input = dd.text
                valueList.append(input.encode("ascii", "ignore").decode())
            houses[id] = valueList
            print(houses[id])
            nextURL = soup.find('a', attrs={'analytics-click-label': 'next'})['href']
            print(nextURL)
            
            if(i & 5 == 0):
                time.sleep(5)
            browser.get(nextURL)
        except Exception as e:
            print(e)
            

    browser.quit()
    with open("houses.json", 'w') as outfile:
        json.dump(houses, outfile)


if __name__ == "__main__":
    scraper()


from pprint import pprint

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scraper_api import ScraperAPIClient


def scrapeUrl(url):
    print(" > Scraping URL: " + url)
    SCRAPER_API_KEY = "48948f46c6686cc1e3748ee16928f8b3"
    client = ScraperAPIClient(SCRAPER_API_KEY)
    result = client.get(url = url).text
    print(" > Finished Scraping")
    leechUrl(result)
   
    
def leechUrl(html_data):
    print(" > Leeching URL.")
    soup = BeautifulSoup(html_data, 'html.parser')
    allText = ''.join(soup.text)
    return summarizeText(allText)

def summarizeText(text):
    print(" > Summarizing Text.")
    response = requests.post(
    "https://api.deepai.org/api/summarization",
        data={
            'text': text,
        },
        headers={'api-key': '6562713e-5f93-41cd-870c-c0c9144a511b'}
    )
    pprint(response)
    
pprint(scrapeUrl("https://www.indmoney.com/articles/stocks/lic-share-price-soars-after-strong-q2-earnings-check-analysts-outlook"))
#get text in an html page using a get request and beautiful soup

# def scrapeUrl(url):
#     url = "https://www.indmoney.com/articles/stocks/lic-share-price-soars-after-strong-q2-earnings-check-analysts-outlook"

#     payload={}
#     headers = {
#         "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#     }

#     response = requests.request("GET", url, headers=headers, data=payload)
#     # response.raise_for_status()
#     soup = BeautifulSoup(response.text, 'html.parser')
#     
#     return texts

# pprint(scrapeUrl("https://www.indmoney.com/articles/stocks/lic-share-price-soars-after-strong-q2-earnings-check-analysts-outlook"))
    

from pprint import pprint

import requests
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
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
    pprint(allText)
    # return summarizeText(allText)

def summarizeText(text):
    print(" > Summarizing Text.")
    response = requests.post(
    "https://api.deepai.org/api/summarization",
        data={
            'text': text,
        },
        headers={'api-key': 'f3a8424b-8280-420c-9401-3f695b896339'}
    )
    pprint(response)
    
demotext = """Life Insurance Corporation, LIC, reported its September quarter earnings on Saturday. The profits increased multifold. We will look for the reasons for it. LIC's share price rocketed on Monday morning after stellar quarterly numbers. Towards the day's close, LIC shares were trading at 6.22% higher at Rs 666.75 per share. In 2022, LIC shares have fallen nearly 25%.

LIC Q2 earnings: Highlights


Below are the detailed numbers from LIC's September quarter earnings.
Net Profit jump: The company reported a net profit of Rs 15,592 crore for Q2FY23. The profit increased multi-fold from Rs 1433 crore in the year-ago period. The jump in profit was because of a change in the way the company computes profits. Sequentially, the net profit increased from Rs 682.9 crore.  

Revenue: LIC's total revenue in Q2FY23 came in at Rs 2.2 lakh crore, which was 19% higher compared to the Rs 1.85 lakh crore revenue reported in Q2FY22.

Net Premiums: The company's net premiums were increased by 27% and stood at Rs 1.3 lakh crore. In the same period last year, the net premium collected was Rs 1.04 lakh crore. The net income from investments rose 10% YoY to Rs 84,104 crore.

Its income from first-year premium rose to Rs 9,125 crore, marking an 11.3% YoY increase. The single premium increase saw massive growth of 62% and stood at Rs 66,901 crore.

NPA: The gross non-performing assets (NPA) ratio of the insurer in its debt portfolio improved by 24 basis points sequentially to 5.60%. LIC had provided Rs 5,132.6 crore towards doubtful debts and bad debts written off up from Rs 117 crore during Q2FY22. 

Persistency ratio: The persistency ratio is the ratio of life insurance policies receiving timely premiums in the year and the number of net active policies. The ratio indicates how many policyholders are paying the due premiums regularly on the policies with the insurer. The thirteenth-month persistency ratio of the insurer improved to 70.52% from 68.81% and to 55.83% from 53.88%, respectively.

Solvency Ratio: It is a measure of an insurer's ability to meet its long-term debt obligations. It increased to 1.88 from 1.83 a year earlier.

AUM increase: The Asset Under Management (AUM) increased from Rs 41.02 lakh crore to Rs 42.93 lakh crore, a growth of 4.67% sequentially.

Management update: “The results signify our gradual and consistent move towards diversifying our product mix aimed at increasing the Non-Par Business share. The same philosophy of diversification is visible in our distribution channel mix where the share of new business premium being sourced from banca and alternate channels has also increased.", M.R. Kumar, chairperson, LIC.

Brokerage Radar: LIC target price

ICICI Securities: The brokerage has kept a BUY rating with a target price of Rs 917 per share. The firm said that increasing non-participating mix and change in surplus distribution policy are significant growth drivers of the value of a new business (VNB) and in turn embedded value (EV). This, against the strong growth outlook of Indian life insurance (especially, through the lens of sum assured), makes LIC a strong investment proposition. """
    
# pprint(summarizeText(demotext))
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
    
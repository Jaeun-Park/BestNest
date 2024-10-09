# %%
import requests
from bs4 import BeautifulSoup
import random
import time

# %%
URL = 'https://wallethub.com/edu/e/most-and-least-educated-cities/6656'
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0'
]
headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
time.sleep(random.uniform(1, 5))
response = requests.get(URL,headers=headers)
# send a GET request to the webpage with headers
class LiteracyRateScraper :
    def __init__(self) -> None:
        pass
    def literacyRateScraper(self):
        response = requests.get(URL)
        if response.status_code == 200:
            # parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
# %%

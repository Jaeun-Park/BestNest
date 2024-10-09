# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# %%
URL = 'https://www.moneygeek.com/living/safest-cities/'
# send a GET request to the webpage with headers
class CrimeCostScraper :
    def __init__(self) -> None:
        pass
    def crimeCostScraper(self):
        response = requests.get(URL)
    #print(response)
        if response.status_code == 200:
            # parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
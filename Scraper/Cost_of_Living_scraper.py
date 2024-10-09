# %%
import requests
from bs4 import BeautifulSoup

# %%
url = 'https://advisorsmith.com/data/coli/'
# send a GET request to the webpage with headers
class CostOfLivingScraper :
    def __init__(self) -> None:
        pass
    def costOfLivingScraper(self):
        response = requests.get(url)
        # use BS to parse content
        soup = BeautifulSoup(response.text, 'html.parser')
        # check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}") 
        else:
            # parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup


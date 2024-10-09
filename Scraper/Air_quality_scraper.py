# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# %%
URL = "https://aqs.epa.gov/aqsweb/airdata/download_files.html#Annual"
# send a GET request to the webpage with headers
class AirQualityScraper :
    def __init__(self) -> None:
        pass
    def airQualityScraper(self):
        response = requests.get(URL)
    #print(response)
        if response.status_code == 200:
            # parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
import os
import pandas as pd
import numpy as np
from Crime_cost_scraper import CrimeCostScraper

class CrimeCostInvoker:
    def __init__(self) -> None:
        pass

    def crimeCostInvoker(self, temp_dir):
        cr = CrimeCostScraper()
        response = cr.crimeCostScraper()

        # Find the <div> containing the information
        results_div = response.find('div', id="mg-odata-google-sheet-213")
        crime_cost_table = results_div.find_next('table', class_='w-full lining-nums tabular-nums style_table__H8eRl')

        # Extract the headers and rows
        headers = [th.text.strip() for th in crime_cost_table.find('thead').find_all('th')]
        rows = [[td.text.strip() for td in tr.find_all('td')] for tr in crime_cost_table.find('tbody').find_all('tr')]

        # Create DataFrame
        df_crime_cost = pd.DataFrame(rows, columns=headers)
        df_city_crime_cost = df_crime_cost[["City", "Crime Cost per Capita"]]

        # Save DataFrame to temp directory
        file_path = os.path.join(temp_dir, 'Crime_Rate.csv')
        df_city_crime_cost.to_csv(file_path, index=False)

        # Additional processing
        df_city_crime_cost["Crime Cost per Capita"] = df_city_crime_cost["Crime Cost per Capita"].replace(r'[\$,]', '', regex=True).astype(float)
        return file_path
import os
import pandas as pd
import numpy as np
from Cost_of_Living_scraper import CostOfLivingScraper

class CostOfLivingInvoker:
    def __init__(self) -> None:
        pass

    def costOfLivingInvoker(self, temp_dir):
        col = CostOfLivingScraper()
        response = col.costOfLivingScraper()

        # Parsing the response
        table_list = response.findAll('table')
        headers = []
        rows = []

        for i, table in enumerate(table_list):
            if i == 0:
                for th in table.find_all('th'):
                    headers.append(th.text.strip())
            for tr in table.find_all('tr'):
                cells = tr.find_all('td')
                if cells:
                    row = [cell.text.strip() for cell in cells]
                    rows.append(row)

        # Create the DataFrame
        df = pd.DataFrame(rows, columns=headers)
        df['Cost of Living Index'] = pd.to_numeric(df['Cost of Living Index'], errors='coerce')

        # Adding scoring logic
        df = df.sort_values(by='Cost of Living Index', ascending=False)
        df['ID'] = range(1, len(df) + 1)
        bins = [0, 51, 102, 153, 204, 255, 306, 357, 408, 459, 510]
        labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        df['Score'] = pd.cut(df['ID'], bins=bins, labels=labels, right=False)

        # Save the DataFrame to the temp directory
        file_path = os.path.join(temp_dir, 'Cost_of_Living.csv')
        df.to_csv(file_path, index=False)
        return file_path
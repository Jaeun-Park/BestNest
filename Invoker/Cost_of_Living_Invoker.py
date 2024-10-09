import sys
import os
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), '../Scraper'))

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

        for i in range(len(table_list)):
            table = table_list[i]
        
            # Extract headers
            if i == 0:
                for th in table.find_all('th'):
                    headers.append(th.text.strip())

            # Extract rows
            for tr in table.find_all('tr'):
                cells = tr.find_all('td')
                if cells:  # If cells are found
                    row = [cell.text.strip() for cell in cells]

                    # Skip the header row from subsequent tables
                    if i > 0 and tr == table.find_all('tr')[1]:  # Compare to the first row (index 1) of the second table and onwards
                        continue
                
                    rows.append(row)

        # Create the DataFrame
        df = pd.DataFrame(rows, columns=headers)
        df['Cost of Living Index'] = pd.to_numeric(df['Cost of Living Index'], errors='coerce')

        # Adding the scoring logic
        df2 = df.sort_values(by='Cost of Living Index', ascending=False)
        df2['ID'] = range(1, len(df2) + 1)
        bins = [0, 51, 102, 153, 204, 255, 306, 357, 408, 459, 510]
        labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        df2['Score'] = pd.cut(df2['ID'], bins=bins, labels=labels, right=False)

        # Specify the file path for the CSV in the temporary directory
        file_path = os.path.join(temp_dir, 'Cost_of_Living.csv')

        # Save the DataFrame to CSV in the temporary directory
        df2.to_csv(file_path, index=False)
        return file_path
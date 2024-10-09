import sys
import os
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), '../Scraper'))
from Literacy_rate_scraper import LiteracyRateScraper

class LiteracyRateInvoker:
    def __init__(self) -> None:
        pass

    def literacyRateInvoker(self, temp_dir):
        col = LiteracyRateScraper()
        response = col.literacyRateScraper()

        if response is not None:
            table_list = response.findAll('table')
            headers = []
            rows = []

            for table in table_list:
                for th in table.find_all('th'):
                    headers.append(th.text.strip())

                # Extract rows
                for tr in table.find_all('tr'):
                    cells = tr.find_all('td')

                    if len(cells) > 0:
                        row = [cell.text.strip() for cell in cells]
                        rows.append(row)

            # Create dataframe
            df = pd.DataFrame(rows, columns=headers)
            df1 = df.drop(columns=['Educational Attainment Rank', 'Quality of Education & Attainment Gap Rank'])

            # Splitting MSA to extract 'State' and 'City'
            df1['State'] = df1['MSA'].str.split(',').str[1]
            df1['MSA'] = df1['MSA'].str.split(',').str[0]

            # Adding the scoring logic
            df1['ID'] = range(1, len(df1) + 1)
            bins = [0, 15, 30, 45, 60, 75, 80, 95, 110, 135, 150]
            labels = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
            df1['Score'] = pd.cut(df1['ID'], bins=bins, labels=labels, right=True)

            # Write the DataFrame to a temporary CSV file
            file_path = os.path.join(temp_dir, 'Literacy_Rate.csv')
            df1.to_csv(file_path, index=False)

            # Return the path to the generated CSV
            return file_path
        else:
            print("Using Already present file")
            return None
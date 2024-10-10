from queue import Full
import sys
import os

from ..Scraper.Literacy_rate_scraper import LiteracyRateScraper
import pandas as pd

class LiteracyRateInvoker:
    def __init__(self) -> None:
        pass
    def literacyRateInvoker(self):

        col = LiteracyRateScraper()
        response = col.literacyRateScraper()
        if (response != None):
            table_list = response.findAll('table')
            headers = []
            rows = []
            for table in table_list:
                    for th in table.find_all('th'):
                        headers.append(th.text.strip())
                    # extract rows
                    for tr in table.find_all('tr'):
                        cells = tr.find_all('td')
    
                        if len(cells) > 0:
                            row = [cell.text.strip() for cell in cells]
                            rows.append(row)

            # create dataframe
            df = pd.DataFrame(rows, columns=headers)
            df1=df.drop(columns=['Educational Attainment Rank','Quality of Education & Attainment Gap Rank'])
            #df1['MSA'].str.split(',')[1]
            df1['State'] = df1['MSA'].str.split(',').str[1]
            df1['MSA'] = df1['MSA'].str.split(',').str[0]
        
            #df1

            # Specify the output directory
            output_dir = os.path.join(os.path.dirname(__file__), '../Data_Files')
            os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist

            # Adding the scoring logic
            df1['ID'] = range(1, len(df1) + 1)
            bins = [0, 15, 30, 45, 60, 75, 80, 95, 110, 135, 150]
            labels = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
            df1['Score'] = pd.cut(df1['ID'], bins=bins, labels=labels, right=True)
            df1.to_csv("Data_Files/Literacy_Rate.csv",index=False) # Writing it to csv.
        else:
             print("Using Already present file")
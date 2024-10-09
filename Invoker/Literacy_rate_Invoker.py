import os
import pandas as pd
from Literacy_rate_scraper import LiteracyRateScraper

class LiteracyRateInvoker:
    def __init__(self) -> None:
        pass

    def literacyRateInvoker(self, temp_dir):
        col = LiteracyRateScraper()
        response = col.literacyRateScraper()

        if response is not None:
            headers = []
            rows = []
            for table in response.findAll('table'):
                for th in table.find_all('th'):
                    headers.append(th.text.strip())
                for tr in table.find_all('tr'):
                    cells = [cell.text.strip() for cell in tr.find_all('td')]
                    if cells:
                        rows.append(cells)

            # Create DataFrame
            df = pd.DataFrame(rows, columns=headers)
            df1 = df.drop(columns=['Educational Attainment Rank', 'Quality of Education & Attainment Gap Rank'])
            df1['State'] = df1['MSA'].str.split(',').str[1]
            df1['MSA'] = df1['MSA'].str.split(',').str[0]

            # Scoring logic
            df1['ID'] = range(1, len(df1) + 1)
            bins = [0, 15, 30, 45, 60, 75, 80, 95, 110, 135, 150]
            labels = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
            df1['Score'] = pd.cut(df1['ID'], bins=bins, labels=labels, right=True)

            # Save DataFrame to temp directory
            file_path = os.path.join(temp_dir, 'Literacy_Rate.csv')
            df1.to_csv(file_path, index=False)
            return file_path
        else:
            return None
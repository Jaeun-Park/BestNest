import sys
import os
import pandas as pd
import numpy as np
import tempfile

sys.path.append(os.path.join(os.path.dirname(__file__), '../Scraper'))

from Crime_cost_scraper import CrimeCostScraper

class CrimeCostInvoker:
    def __init__(self) -> None:
        pass

    def crimeCostInvoker(self, temp_dir):
        cr = CrimeCostScraper()
        response = cr.crimeCostScraper()

        # Find the <div> containing the information
        results_div = response.find('div', id="mg-odata-google-sheet-213")

        # Find the table with the specified class
        crime_cost_table = results_div.find_next('table', class_='w-full lining-nums tabular-nums style_table__H8eRl')

        # Extract the headers from <thead>
        headers = []
        thead = crime_cost_table.find('thead')
        for th in thead.find_all('th'):
            headers.append(th.text.strip())

        # Extract the data rows from <tbody>
        rows = []
        tbody = crime_cost_table.find('tbody')
        for tr in tbody.find_all('tr'):
            row = [td.text.strip() for td in tr.find_all('td')]
            rows.append(row)

        # Create a DataFrame from the extracted data
        df_crime_cost = pd.DataFrame(rows, columns=headers)

        # Extract specific columns (City and Crime Cost per Capita)
        df_city_crime_cost = df_crime_cost[["City", "Crime Cost per Capita"]]

        # Save the DataFrame to a CSV file in the temporary directory
        temp_csv_path = os.path.join(temp_dir, 'crime_cost_per_capita_by_city_2022.csv')
        df_city_crime_cost.to_csv(temp_csv_path, index=False)

        # Read in the dataset from the CSV file
        df_crime_cost = pd.read_csv(temp_csv_path)

        # Create a proper copy of the subset of the DataFrame for calculations
        df_crime_copy = df_crime_cost.loc[:, ["City", "Crime Cost per Capita"]].copy()

        # Convert "Crime Cost per Capita" to numeric values (remove any dollar signs and commas)
        df_crime_copy["Crime Cost per Capita"] = df_crime_copy["Crime Cost per Capita"].replace(r'[\$,]', '', regex=True).astype(float)

        # Step 4: Define conditions for scoring based on "Crime Cost per Capita"
        conditions = [
            (df_crime_copy["Crime Cost per Capita"] < 597),
            (df_crime_copy["Crime Cost per Capita"] < 775),
            (df_crime_copy["Crime Cost per Capita"] < 1099),
            (df_crime_copy["Crime Cost per Capita"] < 1409),
            (df_crime_copy["Crime Cost per Capita"] < 1807),
            (df_crime_copy["Crime Cost per Capita"] < 2179),
            (df_crime_copy["Crime Cost per Capita"] < 2590),
            (df_crime_copy["Crime Cost per Capita"] < 3267),
            (df_crime_copy["Crime Cost per Capita"] < 4416),
            (df_crime_copy["Crime Cost per Capita"] < 11392)
        ]
        scores = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

        # Use np.select() to assign scores based on conditions, default to 0 if no conditions match
        df_crime_copy["score"] = np.select(conditions, scores, default=0)

        # Sort the DataFrame by "score" in descending order
        df_crime_copy = df_crime_copy.sort_values(by="score", ascending=False)

        # Data cleansing
        df_crime_copy['State'] = df_crime_copy['City'].str.split(',').str[1]
        df_crime_copy['City'] = df_crime_copy['City'].str.split(',').str[0]

        # Save the result CSV in the temporary directory
        final_csv_path = os.path.join(temp_dir, 'Crime_Rate.csv')
        df_crime_copy.to_csv(final_csv_path, index=False)

        # Return the path to the generated CSV
        return final_csv_path
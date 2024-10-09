import sys
import os
import requests
import pandas as pd
import numpy as np
import zipfile
import tempfile

# Add the Scraper folder path to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Scraper')))

# Now import AirQualityScraper
from Air_quality_scraper import AirQualityScraper

class AirQualityInvoker:
    def __init__(self) -> None:
        pass

    def airQualityInvoker(self, temp_dir):
        # Step 1: Initialize AirQualityScraper and get the parsed HTML content
        scraper = AirQualityScraper()
        soup = scraper.airQualityScraper()

        if soup is None:
            print("Failed to get HTML content from the scraper.")
            return

        # Step 2: Find the <h2> with id="Annual"
        results_h2 = soup.find('h2', id="Annual")

        if not results_h2:
            print("Failed to find the Annual section.")
            return

        # Step 3: Find the next table with the class "tablebord zebra"
        annual_table = results_h2.find_next('table', class_='tablebord zebra')

        if not annual_table:
            print("Failed to find the annual table.")
            return

        # Step 4: Search for the download link containing the specific text
        download_link = None
        for a_tag in annual_table.find_all('a'):
            if "annual_aqi_by_cbsa_2024.zip" in a_tag['href']:
                download_link = a_tag['href']
                break

        # Step 5: Check if the download link was found
        if download_link:
            # Form the complete URL for downloading the file
            base_url = "https://aqs.epa.gov/aqsweb/airdata/"
            file_url = f"{base_url}{download_link}"

            # Step 6: Download the ZIP file
            zip_response = requests.get(file_url)
            zip_filename = os.path.join(temp_dir, "annual_aqi_by_cbsa_2024.zip")

            # Step 7: Save the ZIP file in the temporary directory
            with open(zip_filename, 'wb') as file:
                file.write(zip_response.content)

            # Step 8: Extract the CSV file from the ZIP into the temp directory
            try:
                with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            except Exception as e:
                print("Failed to extract ZIP file:", e)
                return

            # Step 9: Remove the ZIP file after extraction
            os.remove(zip_filename)

            # Step 10: Read in the dataset from the temp directory
            csv_file_path = os.path.join(temp_dir, 'annual_aqi_by_cbsa_2024.csv')
            try:
                df_air_quality = pd.read_csv(csv_file_path)
            except FileNotFoundError:
                print("CSV file not found. Please check if the ZIP was extracted correctly.")
                return

            # Step 11-18: Processing the DataFrame
            df_cbsa_good_days = df_air_quality.loc[:, ["CBSA", "Days with AQI", "Good Days"]].copy()
            df_cbsa_good_days["City"] = df_cbsa_good_days["CBSA"].str.split(',').str[0]
            df_cbsa_good_days["percentage"] = (df_cbsa_good_days["Good Days"] / df_cbsa_good_days["Days with AQI"]) * 100

            conditions = [
                (df_cbsa_good_days["percentage"] >= 98),
                (df_cbsa_good_days["percentage"] >= 95),
                (df_cbsa_good_days["percentage"] >= 90),
                (df_cbsa_good_days["percentage"] >= 85),
                (df_cbsa_good_days["percentage"] >= 80),
                (df_cbsa_good_days["percentage"] >= 75),
                (df_cbsa_good_days["percentage"] >= 70),
                (df_cbsa_good_days["percentage"] >= 65),
                (df_cbsa_good_days["percentage"] >= 60),
                (df_cbsa_good_days["percentage"] >= 50)
            ]
            scores = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
            df_cbsa_good_days["score"] = np.select(conditions, scores, default=0)
            df_cbsa_good_days = df_cbsa_good_days.drop(columns=["percentage"])
            df_cbsa_good_days = df_cbsa_good_days.loc[df_cbsa_good_days.groupby("City")["score"].idxmax()]
            df_cbsa_good_days = df_cbsa_good_days.sort_values(by="score", ascending=False)

            # Step 19-20: Save the result in the temporary directory
            file_path = os.path.join(temp_dir, 'Air_quality.csv')
            df_cbsa_good_days.to_csv(file_path, index=False)

        else:
            print("Download link for 'annual_aqi_by_cbsa_2024.zip' not found.")

if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as temp_dir:
        invoker = AirQualityInvoker()
        invoker.airQualityInvoker(temp_dir)
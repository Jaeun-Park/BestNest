import sys
import os
import requests
import pandas as pd
import numpy as np
import zipfile

from ..Scraper.Air_quality_scraper import AirQualityScraper

class AirQualityInvoker:
    def __init__(self) -> None:
        pass

    def airQualityInvoker(self):
        #print("Step 1: Initializing AirQualityScraper and getting parsed HTML content")
        # Step 1: Initialize AirQualityScraper and get the parsed HTML content
        scraper = AirQualityScraper()
        soup = scraper.airQualityScraper()

        if soup is None:
            print("Failed to get HTML content from the scraper.")
            return

        #print("Step 2: Finding <h2> with id='Annual'")
        # Step 2: Find the <h2> with id="Annual"
        results_h2 = soup.find('h2', id="Annual")

        if not results_h2:
            print("Failed to find the Annual section.")
            return

        #print("Step 3: Finding the next table with class='tablebord zebra'")
        # Step 3: Find the next table with the class "tablebord zebra"
        annual_table = results_h2.find_next('table', class_='tablebord zebra')

        if not annual_table:
            print("Failed to find the annual table.")
            return

        #print("Step 4: Searching for the download link containing the specific text")
        # Step 4: Search for the download link containing the specific text
        download_link = None
        for a_tag in annual_table.find_all('a'):
            if "annual_aqi_by_cbsa_2024.zip" in a_tag['href']:
                download_link = a_tag['href']
                break

        # Step 5: Check if the download link was found
        if download_link:
            #print("Download link found:", download_link)
            # Form the complete URL for downloading the file
            base_url = "https://aqs.epa.gov/aqsweb/airdata/"
            file_url = f"{base_url}{download_link}"

            #print("Step 6: Downloading the ZIP file")
            # Step 6: Download the ZIP file
            zip_response = requests.get(file_url)
            zip_filename = "annual_aqi_by_cbsa_2024.zip"

            # Step 7: Save the ZIP file locally
            with open(zip_filename, 'wb') as file:
                file.write(zip_response.content)

            #print(f"Downloaded ZIP file: {zip_filename}")

            # Step 8: Extract the CSV file from the ZIP
            try:
                with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                    zip_ref.extractall()
                #print("Extracted the CSV files to the current directory")
            except Exception as e:
                print("Failed to extract ZIP file:", e)
                return

            # Step 9: Clean up by removing the ZIP file
            os.remove(zip_filename)
            #print("Cleaned up the ZIP file")

            # Step 10: Read in the dataset
            try:
                df_air_quality = pd.read_csv('annual_aqi_by_cbsa_2024.csv')
                #print("Successfully read the CSV file")
            except FileNotFoundError:
                print("CSV file not found. Please check if the ZIP was extracted correctly.")
                return

            # Step 11-18: Processing the DataFrame
            #print("Processing the data")
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

            # Step 19-20: Saving the result to CSV
            output_dir = os.path.join(os.path.dirname(__file__), '../Data_Files')
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, 'Air_quality.csv')
            df_cbsa_good_days.to_csv(file_path, index=False)
            #print(f"Sorted data has been saved to '{file_path}'")

        else:
            print("Download link for 'annual_aqi_by_cbsa_2024.zip' not found.")

if __name__ == "__main__":
    invoker = AirQualityInvoker()
    invoker.airQualityInvoker()
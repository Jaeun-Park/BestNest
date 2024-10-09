import os
import requests
import pandas as pd
import zipfile
from Air_quality_scraper import AirQualityScraper

class AirQualityInvoker:
    def __init__(self) -> None:
        pass

    def airQualityInvoker(self, temp_dir):
        scraper = AirQualityScraper()
        soup = scraper.airQualityScraper()

        if soup:
            results_h2 = soup.find('h2', id="Annual")
            annual_table = results_h2.find_next('table', class_='tablebord zebra')

            download_link = None
            for a_tag in annual_table.find_all('a'):
                if "annual_aqi_by_cbsa_2024.zip" in a_tag['href']:
                    download_link = a_tag['href']
                    break

            if download_link:
                file_url = f"https://aqs.epa.gov/aqsweb/airdata/{download_link}"
                zip_filename = os.path.join(temp_dir, "annual_aqi_by_cbsa_2024.zip")

                # Download and extract ZIP file
                zip_response = requests.get(file_url)
                with open(zip_filename, 'wb') as file:
                    file.write(zip_response.content)

                with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                os.remove(zip_filename)

                # Read and process CSV file
                csv_file_path = os.path.join(temp_dir, 'annual_aqi_by_cbsa_2024.csv')
                df_air_quality = pd.read_csv(csv_file_path)
                df_cbsa_good_days = df_air_quality.loc[:, ["CBSA", "Days with AQI", "Good Days"]].copy()

                # Scoring and processing
                df_cbsa_good_days["City"] = df_cbsa_good_days["CBSA"].str.split(',').str[0]
                df_cbsa_good_days["percentage"] = (df_cbsa_good_days["Good Days"] / df_cbsa_good_days["Days with AQI"]) * 100

                conditions = [
                    (df_cbsa_good_days["percentage"] >= 98),
                    (df_cbsa_good_days["percentage"] >= 95),
                    # ... (remaining conditions)
                ]
                scores = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
                df_cbsa_good_days["score"] = np.select(conditions, scores, default=0)

                # Save DataFrame to temp directory
                file_path = os.path.join(temp_dir, 'Air_quality.csv')
                df_cbsa_good_days.to_csv(file_path, index=False)
                return file_path
from Invoker.Cost_of_Living_Invoker import CostOfLivingInvoker
from Invoker.Literacy_rate_Invoker import LiteracyRateInvoker
from Invoker.Air_quality_Invoker import AirQualityInvoker
from Invoker.Crime_Cost_Invoker import CrimeCostInvoker
import pandas as pd
from functools import reduce
import numpy as np
import tempfile
import os

class MergeData():
    @staticmethod
    def mergeData(user_choices_path):
        expected_columns = ['City_x', 'State_x', 'Cost of Living Index', 'ID', 'Score', 'City-State', 'City_y', 
                            'Crime Cost per Capita', 'score_x', 'State_y', 'CBSA', 'Days with AQI', 'Good Days',         
                            'City', 'score_y', 'State', 'Literacy Rate Value', 'Literacy Rate Score']

        # Use a temporary directory to handle file operations
        with tempfile.TemporaryDirectory() as temp_dir:
            # Path where temporary files will be saved
            data_files_path = temp_dir
            
            # Reading user choices from the passed file path
            choices = pd.read_csv(user_choices_path)
            choices_list = choices['0'].tolist()
            
            print("Loading Data....")
            df_merged = []
            
            print(f"User choices file path: {user_choices_path}")
            
            for choice in choices_list:
                if int(choice) == 1:
                    # Invoke the cost of living data scraper and pass the temp dir
                    col = CostOfLivingInvoker()
                    col.costOfLivingInvoker(data_files_path)
                    
                    # Read Cost of Living data from the temporary directory
                    col_path = os.path.join(data_files_path, 'Cost_of_Living.csv')
                    df_col = pd.read_csv(col_path)
                    
                    # Concatenate City and State to get unique city
                    df_col['City-State'] = df_col['City'] + "-" + df_col['State'].str.strip()
                    df_col = df_col.rename(columns={'Score': 'Cost of Living Score', 'City': 'Cost of Living City', 'State': 'Cost of Living State'})
                    df_merged.append(df_col)
                
                elif int(choice) == 2:
                    # Invoke the literacy rate data scraper and pass the temp dir
                    lr = LiteracyRateInvoker()
                    lr.literacyRateInvoker(data_files_path)
                    
                    # Read Literacy Rate data from the temporary directory
                    lr_path = os.path.join(data_files_path, 'Literacy_Rate.csv')
                    df_lr = pd.read_csv(lr_path)
                    
                    # Process the literacy rate data
                    df_lr = df_lr.rename(columns={'MSA': 'City', 'Score': 'Literacy Rate Score'})
                    df_lr['City-State'] = df_lr['City'] + "-" + df_lr['State'].str.strip()
                    df_lr = df_lr.rename(columns={'City': 'Literacy City', 'State': 'Literacy State'})
                    df_merged.append(df_lr)
                
                elif int(choice) == 3:
                    # Invoke the crime cost data scraper and pass the temp dir
                    cr = CrimeCostInvoker()
                    cr.crimeCostInvoker(data_files_path)
                    
                    # Read Crime Cost data from the temporary directory
                    cr_path = os.path.join(data_files_path, 'Crime_Rate.csv')
                    df_cr = pd.read_csv(cr_path)
                    
                    # Process the crime cost data
                    df_cr['City-State'] = df_cr['City'] + "-" + df_cr['State'].str.strip()
                    df_cr = df_cr.rename(columns={'score': 'Crime Cost Score', 'City': 'CR City', 'State': 'CR State'})
                    df_merged.append(df_cr)
                
                elif int(choice) == 4:
                    # Invoke the air quality data scraper and pass the temp dir
                    aqi = AirQualityInvoker()
                    aqi.airQualityInvoker(data_files_path)
                    
                    # Read Air Quality data from the temporary directory
                    aqi_path = os.path.join(data_files_path, 'Air_quality.csv')
                    df_aqi = pd.read_csv(aqi_path)
                    
                    # Process the air quality data
                    df_aqi['State'] = df_aqi['CBSA'].str.split(",").str[1]
                    df_aqi['City-State'] = df_aqi['City'] + "-" + df_aqi['State'].str.strip()
                    df_aqi = df_aqi.rename(columns={'score': 'Air Quality Score', 'City': 'AQI City', 'State': 'AQI State'})
                    df_merged.append(df_aqi)
            
            # Merging the dataframes into one
            final_df = reduce(lambda left, right: pd.merge(left, right, on='City-State', how='inner'), df_merged)
            
            for col in expected_columns:
                if col not in final_df.columns:
                    final_df[col] = None
            
            final_df['City'] = final_df['City-State'].str.split("-").str[0]
            final_df['State'] = final_df['City-State'].str.split("-").str[1]
            
            # Reindexing and renaming columns
            final_df = final_df.drop(['ID', 'CBSA', 'Days with AQI'], axis=1)
            final_df = final_df.rename(columns={'Cost of Living Index': 'Cost of Living Value', 
                                                'Total Score': 'Literacy Rate Value', 
                                                'Crime Cost per Capita': 'Crime Cost Value', 
                                                'Good Days': 'Air Quality Value'})
            
            # Storing combined data in one temporary file
            combined_file_path = os.path.join(data_files_path, 'Combined.csv')
            final_df.to_csv(combined_file_path, index=False)

            return combined_file_path  # Return the path to the merged data
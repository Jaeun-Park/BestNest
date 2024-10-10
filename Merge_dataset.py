from Invoker.Cost_of_Living_Invoker import CostOfLivingInvoker
from Invoker.Literacy_rate_Invoker import LiteracyRateInvoker
from Invoker.Air_quality_Invoker import AirQualityInvoker
from Invoker.Crime_Cost_Invoker import CrimeCostInvoker
import pandas as pd
from functools import reduce
import numpy as np

#Scraping Cost of living and storing it in csv
class MergeData():

    def mergeData():
        expected_columns =['City_x','State_x','Cost of Living Index','ID','Score','City-State','City_y','Crime Cost per Capita','score_x','State_y','CBSA','Days with AQI','Good Days','City','score_y','State','Literacy Rate Value', 'Literacy Rate Score']
        choices = pd.read_csv('Data_Files/User_Choices.csv')
        choices_list = choices['0'].tolist()
        print("Loading Data....")
        df_merged =[]
        for choice in choices_list:
            if (int(choice) == 1):
                col = CostOfLivingInvoker()
                col.costOfLivingInvoker()
                df_col=pd.read_csv('Data_Files/Cost_of_Living.csv')
                #Concatenating City and State to get unique city
                df_col['City-State'] = df_col['City']+"-"+df_col['State'].str.strip()
                df_col = df_col.rename(columns={'Score': 'Cost of Living Score'})
                df_col = df_col.rename(columns={'City': 'Cost of Living City'})
                df_col = df_col.rename(columns={'State': 'Cost of Living State'})
                df_merged.append(df_col)
            elif(int(choice)==2):
                #print("Not working right now")
                #Scraping Literacy Rate and storing it in csv
                lr = LiteracyRateInvoker()
                lr.literacyRateInvoker()
                
                df_lr =pd.read_csv('Data_Files/Literacy_Rate.csv')
                #print(df_lr)
                df_lr = df_lr.rename(columns={'MSA': 'City','Score':'Literacy Rate Score'})
                df_lr['City-State'] = df_lr['City']+"-"+df_lr['State'].str.strip()
                df_lr = df_lr.rename(columns={'City': 'Literacy City'})
                df_lr = df_lr.rename(columns={'State': 'Literacy State'})
                #df_lr_unique = df_lr.unique()
                df_merged.append(df_lr)
                
            
            elif(int(choice)==3):
                #Scraping Crime Cost and storing it in csv
                cr = CrimeCostInvoker()
                cr.crimeCostInvoker()
                df_cr = pd.read_csv('Data_Files/Crime_Rate.csv')
                #Concatenating City and State to get unique city
                df_cr['City-State'] = df_cr['City']+"-"+df_cr['State'].str.strip()
                df_cr = df_cr.rename(columns={'score': 'Crime Cost Score'})
                df_cr = df_cr.rename(columns={'City': 'CR City'})
                df_cr = df_cr.rename(columns={'State': 'CR State'})
                df_merged.append(df_cr)
            
            elif(int(choice)==4):
                #Scraping Air Quality and storing it in csv
                aqi = AirQualityInvoker()
                aqi.airQualityInvoker()
                df_aqi = pd.read_csv('Data_Files/Air_quality.csv')
        
                #Spliting State from City
                df_aqi['State'] = df_aqi['CBSA'].str.split(",").str[1]
                #Concatenating City and State to get unique city
                df_aqi['City-State'] = df_aqi['City']+"-"+df_aqi['State'].str.strip()
                df_aqi = df_aqi.rename(columns={'score': 'Air Quality Score'})
                df_aqi = df_aqi.rename(columns={'City': 'AQI City'})
                df_aqi = df_aqi.rename(columns={'State': 'AQI State'})
                df_merged.append(df_aqi)
        #Mergeing the dataframes to one.
        
        final_df = reduce(lambda left, right: pd.merge(left, right, on='City-State', how='inner'), df_merged)
        
        for col in expected_columns:
            if col not in final_df.columns:
                final_df[col] = None
        final_df['City'] = final_df['City-State'].str.split("-").str[0]
        final_df['State'] = final_df['City-State'].str.split("-").str[1]
        #reindexing
        final_df = final_df.drop(['ID','CBSA','Days with AQI'],axis =1)
        final_df = final_df.rename(columns={'Cost of Living Index':'Cost of Living Value','Total Score':'Literacy Rate Value','Crime Cost per Capita':'Crime Cost Value','Good Days':'Air Quality Value'})

        #Storing combined data in one file
        final_df.to_csv('Data_Files/Combined.csv', index=False)





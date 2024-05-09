import pandas as pd
import os, pytz
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.covariance import MinCovDet


def load_data(solar_file_path, weather_file_path):
    
    # Define CEST as UTC+2 with pytz
    cest = pytz.FixedOffset(120)
    
    solar_df = pd.read_csv(solar_file_path, sep=';', index_col=1, parse_dates=True).sort_index()  #'data/solar.csv'
    solar_df.index = solar_df.index.tz_localize(cest)

    # Define UTC as UTC+0 with pytz
    utc = pytz.FixedOffset(0)

    # list all of the filenames in the data/weather folder
    filenames = os.listdir(weather_file_path) #'data/weather'

    # Create an empty dictionnary to store the dataframes
    weather_list = []
    # Loop over the filenames
    for filename in filenames:
        df_buf = pd.read_csv('data/weather/' + filename, sep=r'\s+').iloc[:(24*4)]

        df_buf.index = df_buf['YYYY'].astype(int).astype(str) + "-" + df_buf['MM'].astype(int).astype(str) + "-" + df_buf['DD'].astype(int).astype(str) + " " + df_buf['HH'].astype(int).astype(str) + ":" + df_buf['MIN'].astype(int).astype(str)
        df_buf = df_buf.drop(columns=['YYYY', 'MM', 'DD', 'HH', 'MIN'])

        df_buf.index = pd.to_datetime(df_buf.index, format='%Y-%m-%d %H:%M').tz_localize(utc).tz_convert(cest)
        # add the dataframe to the list
        weather_list.append(df_buf)

    # Concatenate the dataframes in the list File 20220524 is empty, hence the length of the list is 33.600 and not 33.696
    weather_df = pd.concat(weather_list, join='outer').sort_index()

    # Merge the two dataframes
    merged_df = pd.merge(solar_df, weather_df, left_index=True, right_index=True, how='outer')
    merged_df.to_csv('data/merged.csv')
    cleaned_df = merged_df.dropna()


    for column in cleaned_df.columns:
        if cleaned_df[column].dtype == object:
            cleaned_df[column] = cleaned_df[column].apply(pd.to_numeric, errors='coerce')


    return cleaned_df


if __name__ == "__main__":

    cleaned_data = load_data('data/solar.csv', 'data/weather')

    # Create a new file with the cleaned data
    cleaned_data.to_csv('data/cleaned.csv')



    
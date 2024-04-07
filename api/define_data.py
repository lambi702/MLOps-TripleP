import datetime
import os
import numpy as np
import pandas as pd


def define_new_data(df):
    """
    Function to define the new data

    Arguments:
        - df: dataframe containing the data
    """

    df = df.rename(columns={'Unnamed: 0': 'Timestamp'})
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    df['Month'] = df['Timestamp'].dt.month
    df['Day'] = df['Timestamp'].dt.day
    df['Hour'] = df['Timestamp'].dt.hour + df['Timestamp'].dt.minute / 60

    df = df.drop(columns=df.columns[:9])
    df = df.drop(columns=df.columns[1:10])

    return df

def convert_date(row):
    """
    Function to convert the date from the csv file to a datetime object

    Arguments:
        - row: row of the dataframe
    """


    month, day, hour = int(row['Month']), int(row['Day']), row['Hour']
    year = datetime.now().year  # Utilisation de l'année actuelle

    hour_int = int(hour)  # Partie entière des heures
    minute_dec = (hour % 1) * 60  # Partie décimale des heures, convertie en minutes

    date_string = f"{year}-{month}-{day} {hour_int}:{int(minute_dec)}"
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M')  # Conversion en objet datetime




def get_statistics(df):
    """
    Function to compute the mean and std of the data

    Arguments:
        - df: dataframe containing the data
    """

    mean = df.mean()
    std = df.std()

    print(f"Mean: {mean}"
          f"Std: {std}")
    
    max_values = df.max()
    min_values = df.min()
    print(f"Max values: {max_values}"
          f"Min values: {min_values}")
    
    # modify the data based on the mean and std
    np.random.normal(mean, std, size=df.shape)
    data = df + np.random.normal(mean, std, size=df.shape)

    # Copy back the columns SWD, SWDtop, SNOW, Month, Day and Hour
    data['SWD'] = df['SWD']
    data['SWDtop'] = df['SWDtop']
    data['SNOW'] = df['SNOW']
    data['Month'] = df['Month']
    data['Day'] = df['Day']
    data['Hour'] = df['Hour']

    # CD must be between  and 
    data['CD'] = np.clip(data['CD'], 0, 1)
    data['CM'] = np.clip(data['CM'], 0, 1)
    data['CU'] = np.clip(data['CU'], 0, 1)

    # PREC, WS100m and WS10m must be positive
    data['PREC'] = np.clip(data['PREC'], 0, None)
    data['WS100m'] = np.clip(data['WS100m'], 0, None)
    data['WS10m'] = np.clip(data['WS10m'], 0, None)

    # RH2m must be between 0 and 100
    data['RH2m'] = np.clip(data['RH2m'], 0, 100)



    return data

if __name__ == '__main__':
    
    # Load the data
    current_dir = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(current_dir, "../data/no_outliers.csv")
    df_train = pd.read_csv(csv_path, sep=';', index_col=1)
    
    df_new = define_new_data(df_train)
    df_new = df_new.drop(columns=['Power_Total'])

    # Compute mean and std
    data = get_statistics(df_new)

    print(data.head())


    # Save the new data
    new_csv_path = os.path.join(current_dir, "../data/new_data_no_outliers.csv")
    data.to_csv(new_csv_path, sep=';', index=False)
    print(f"New data saved to {new_csv_path}")

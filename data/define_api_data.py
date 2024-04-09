from datetime import datetime, timedelta
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
    data['Power_Total'] = df['Power_Total']

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


def get_7days_data(df):
    """
    Function to get the data of the next 7 days after today

    Arguments:
        - df: dataframe containing the data
    """
    
    # get the date of today   
    today = datetime.now()
    month = today.month
    day = today.day

    # Define the number of days remaining in the month
    days_in_month = {
    1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    days_remaining_in_month = days_in_month[month] - day + 1

    # Get the data of the next 7 days
    if days_remaining_in_month >= 7:
    # If there are at least 7 days remaining in the current month
        end_day = day + 7


    else:
        # If there are fewer than 7 days remaining in the current month
        end_day = 7 - days_remaining_in_month

        # Adjust for the next month
        next_month = (month % 12) + 1
        days_in_next_month = days_in_month[next_month]
        while end_day > days_in_next_month:
            end_day -= days_in_next_month
            next_month = (next_month % 12) + 1
            days_in_next_month = days_in_month[next_month]

    if days_remaining_in_month >= 7:
        newData_7Days = df_new[
            ((df['Month'] == month) & (df['Day'] >= day) & (df['Day'] <= end_day))
        ]
    else:
        newData_7Days = df_new[
            ((df['Month'] == month) & (df['Day'] >= day) & (df['Day'] <= end_day)) |
            ((df['Month'] == next_month) & (df['Day'] <= end_day))
        ]

    # Drop the column Power_Total as not yet predicted
    print(newData_7Days.head())
    newData_7Days = newData_7Days.drop(columns=['Power_Total'])

    # Save the new data
    current_dir = os.path.dirname(os.path.realpath(__file__))
    new_csv_path = os.path.join(current_dir, "../api/data/newData_7Days.csv")
    newData_7Days.to_csv(new_csv_path, sep=';', index=False)
    print(f"New data saved to {new_csv_path}")



def get_training_data(df):
    """
    Function to get the data for training
    
    Arguments:
        - df: dataframe containing the data
    """

    # Get the data of the previous days of the year
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    month = yesterday.month
    day = yesterday.day

    # get data from the beginning of the year to yesterday
    new_training_data = df[
        (df['Month'] < month) |
        ((df['Month'] == month) & (df['Day'] <= day))
    ]

    # Save the new data
    current_dir = os.path.dirname(os.path.realpath(__file__))
    new_csv_path = os.path.join(current_dir, "../api/data/newData_forTrain.csv")
    new_training_data.to_csv(new_csv_path, sep=';', index=False)
    print(f"New data saved to {new_csv_path}")

    
    



if __name__ == '__main__':
    
    # Load the data
    current_dir = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(current_dir, "no_outliers.csv")
    df_train = pd.read_csv(csv_path, sep=';', index_col=1)
    
    df_new = define_new_data(df_train)

    # Compute mean and std
    data = get_statistics(df_new)

    # Save the new data for next 7 days
    get_7days_data(data)

    # Save data for training (= previous days of the year)
    get_training_data(data)

    

    
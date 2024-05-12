"""
define_api_data.py: defines functions to process solar and weather data from a CSV file.
Various functions are defined to process the data to conform to the API requirements.
"""

from datetime import datetime, timedelta
import os
import numpy as np
import pandas as pd


def define_new_data(d_f):
    """
    Function to define the new data and handle the timestamp column

    Arguments:
        - d_f: dataframe containing the data

    Returns:
        - d_f: dataframe containing the new data
    """

    d_f = d_f.rename(columns={"Unnamed: 0": "Timestamp"})
    d_f["Timestamp"] = pd.to_datetime(d_f["Timestamp"])

    d_f["Month"] = d_f["Timestamp"].dt.month
    d_f["Day"] = d_f["Timestamp"].dt.day
    d_f["Hour"] = d_f["Timestamp"].dt.hour + d_f["Timestamp"].dt.minute / 60

    d_f = d_f.drop(columns=d_f.columns[:9])
    d_f = d_f.drop(columns=d_f.columns[1:10])

    return d_f


def convert_date(row):
    """
    Function to convert the date from the csv file to a datetime object

    Arguments:
        - row: row of the dataframe
    """

    month, day, hour = int(row["Month"]), int(row["Day"]), row["Hour"]
    year = datetime.now().year  # Utilisation de l'année actuelle

    hour_int = int(hour)  # Partie entière des heures
    minute_dec = (hour % 1) * 60  # Partie décimale des heures, convertie en minutes

    date_string = f"{year}-{month}-{day} {hour_int}:{int(minute_dec)}"
    return datetime.strptime(
        date_string, "%Y-%m-%d %H:%M"
    )  # Conversion en objet datetime


def get_statistics(d_f):
    """
    Function to compute the mean and std of the data

    Arguments:
        - d_f: dataframe containing the data
    """

    mean = d_f.mean()
    std = d_f.std()


    #print(f"Mean: {mean}"
    #      f"Std: {std}")

    #max_values = d_f.max()
    #min_values = d_f.min()
    #print(f"Max values: {max_values}"
    #      f"Min values: {min_values}")

    # modify the data based on the mean and std
    np.random.normal(mean, std, size=d_f.shape)
    data_stats = d_f + np.random.normal(mean, std, size=d_f.shape)

    # Copy back the columns SWD, SWDtop, SNOW, Month, Day and Hour
    data_stats["SWD"] = d_f["SWD"]
    data_stats["SWDtop"] = d_f["SWDtop"]
    data_stats["SNOW"] = d_f["SNOW"]
    data_stats["Month"] = d_f["Month"]
    data_stats["Day"] = d_f["Day"]
    data_stats["Hour"] = d_f["Hour"]
    data_stats["Power_Total"] = d_f["Power_Total"]

    # CD must be between  and
    data_stats["CD"] = np.clip(data_stats["CD"], 0, 1)
    data_stats["CM"] = np.clip(data_stats["CM"], 0, 1)
    data_stats["CU"] = np.clip(data_stats["CU"], 0, 1)

    # PREC, WS100m and WS10m must be positive
    data_stats["PREC"] = np.clip(data_stats["PREC"], 0, None)
    data_stats["WS100m"] = np.clip(data_stats["WS100m"], 0, None)
    data_stats["WS10m"] = np.clip(data_stats["WS10m"], 0, None)

    # RH2m must be between 0 and 100
    data_stats["RH2m"] = np.clip(data_stats["RH2m"], 0, 100)

    return data_stats


def get_7days_data(d_f):
    """
    Function to get the data of the next 7 days after today

    Arguments:
        - d_f: dataframe containing the data
    """

    # get the date of today
    today = datetime.now()
    month = today.month
    day = today.day

    # Define the number of days remaining in the month
    days_in_month = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }
    days_remaining_in_month = days_in_month[month] - day + 1

    # Get the data of the next 7 days
    if days_remaining_in_month >= 7:
        # If there are at least 7 days remaining in the current month
        end_day = day + 7

        new_data_7_days = d_f_new[
            ((d_f["Month"] == month) & (d_f["Day"] >= day) & (d_f["Day"] <= end_day))
        ]

    else:
        # If there are fewer than 7 days remaining in the current month
        end_day = 7 - days_remaining_in_month
        next_month = (month % 12) + 1

        # Adjust for the next month
        days_in_next_month = days_in_month[next_month]
        while end_day > days_in_next_month:
            end_day -= days_in_next_month
            next_month = (next_month % 12) + 1
            days_in_next_month = days_in_month[next_month]
        nb_days_current_month = days_in_month[month]

        new_data_7_days = d_f_new[
            (
                (d_f["Month"] == month)
                & (d_f["Day"] >= day)
                & (d_f["Day"] <= nb_days_current_month)
            )
            | ((d_f["Month"] == next_month) & (d_f["Day"] <= end_day))
        ]

    # Drop the column Power_Total as not yet predicted
    # print(new_data_7_days.head())
    new_data_7_days = new_data_7_days.drop(columns=["Power_Total"])

    # Save the new data
    current_dir_7 = os.path.dirname(os.path.realpath(__file__))
    new_csv_path_7 = os.path.join(current_dir_7, "../api/data/new_data_7_days.csv")
    new_data_7_days.to_csv(new_csv_path_7, sep=";", index=False)
    # print(f"New data saved to {new_csv_path_7}")


def get_training_data(d_f):
    """
    Function to get the data for training

    Arguments:
        - d_f: dataframe containing the data
    """

    # Get the data of the previous days of the year
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    month = yesterday.month
    day = yesterday.day

    # get data from the beginning of the year to yesterday
    new_training_data = d_f[
        (d_f["Month"] < month) | ((d_f["Month"] == month) & (d_f["Day"] <= day))
    ]

    # Save the new data
    current_dir_train = os.path.dirname(os.path.realpath(__file__))
    new_csv_path_train = os.path.join(current_dir_train, "../api/data/newData_forTrain.csv")
    new_training_data.to_csv(new_csv_path_train, sep=";", index=False)
    # print(f"New data saved to {new_csv_path_train}")


if __name__ == "__main__":

    # Load the data
    current_dir = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(current_dir, "no_outliers.csv")
    d_f_train = pd.read_csv(csv_path, sep=";", index_col=1)

    d_f_new = define_new_data(d_f_train)

    # Compute mean and std
    data = get_statistics(d_f_new)

    # Save the new data for next 7 days
    get_7days_data(data)

    # Save data for training (= previous days of the year)
    get_training_data(data)

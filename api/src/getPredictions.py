"""
    getPredictions.py: Module to get the predictions of the model
"""

from datetime import datetime
import pandas as pd


def convert_date(row):
    """
    Function to convert the date from the csv file to a datetime object: human readable

    Arguments:
        - row: row of the dataframe
    """

    month, day, hour = int(row["Month"]), int(row["Day"]), row["Hour"]
    year = datetime.now().year

    hour_int = int(hour)
    minute_dec = (hour % 1) * 60

    date_string = f"{year}-{month}-{day} {hour_int}:{int(minute_dec)}"
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M")


def get_predictions():
    """
    Function to get the predictions of the model

    """
    # Load the predicted meteorological data of the next 7 days from the cloud
    data = pd.read_csv(
        "https://storage.googleapis.com/mlsd-project/newData_7Days.csv", sep=";"
    )

    # Modify the date in the data so that is human readable
    date_pred = []
    for _, row in data.iterrows():
        date_pred.append(convert_date(row))

    # Load the predictions from the cloud that have been computed by the model every day
    predictions_pred = pd.read_csv(
        "https://storage.googleapis.com/mlsd-project/predictions.csv", sep=";", header=0
    )
    predictions_pred = predictions_pred.squeeze()

    # return what we need in the API
    return predictions_pred, date_pred, data["SWD"], data["SWDtop"]


if __name__ == "__main__":
    predictions, date, SWD, ST = get_predictions()

    df = pd.DataFrame({"predictions": predictions, "days": date, "SWD": SWD, "ST": ST})

    print(df.head())

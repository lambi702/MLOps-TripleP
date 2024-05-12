from datetime import datetime, timedelta
import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from define_api_data import *


"""
    These code is executed every day to update the model with the new data.
    We must first update the data in the csv file to have them up to date.
    Then we can update the model with the new data.
    Once the model is updated, we can make predictions with the new data.
    The predictions and the new data are then saved on the cloud.
"""


def define_data(df):
    """
    Function to define the data and to clean it

    Arguments:
        - df: dataframe containing the data
    """

    df = df.rename(columns={"Unnamed: 0": "Timestamp"})
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    df["Month"] = df["Timestamp"].dt.month
    df["Day"] = df["Timestamp"].dt.day
    df["Hour"] = df["Timestamp"].dt.hour + df["Timestamp"].dt.minute / 60

    df = df.drop(columns=df.columns[:9])
    df = df.drop(columns=df.columns[1:10])

    return df


def get_data():
    """
    Function to get the date of today and update data accordingly

    """
    # Get access to the training data: no_outliers.csv
    df_train = pd.read_csv(
        "https://storage.googleapis.com/mlsd-project/no_outliers.csv",
        sep=";",
        index_col=1,
    )

    # New data
    df_new = define_new_data(df_train)
    data = get_statistics(df_new)

    # Save the next 7 days data:
    get_7days_data(data)

    # Save the data for training
    get_training_data(data)

    # Dataframe of the training data
    df_train = define_data(df_train)

    return df_train


def define_training_data(df_train_old):
    """
    Function to define the training data

    Arguments:
        - df_train_old: dataframe containing the training data
    """

    # Get the data for training
    get_training_data(df_train_old)

    # Load the new data for training
    current_dir = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(current_dir, "data/newData_forTrain.csv")
    df_train = pd.read_csv(csv_path, sep=";", index_col=1)

    # Concatenate the two dataframes
    df_train = pd.concat([df_train_old, df_train])

    return df_train


def define_features_target(df):
    """
    Function to define the features and target of the model

    Arguments:
        - df: dataframe containing the data
    """

    target = df.drop(columns=df.columns[1:])
    features = df.drop(columns=["Power_Total"])

    features_train, features_temp, target_train, target_temp = train_test_split(
        features, target, test_size=0.25, random_state=42
    )
    features_val, features_test, target_val, target_test = train_test_split(
        features_temp, target_temp, test_size=0.5, random_state=42
    )

    return features_train, target_train, features_val, target_val


def define_model(df):
    """
    Function to define the model

    Arguments:
        - df: dataframe containing the data
    """

    # Define the model
    rf = RandomForestRegressor(
        bootstrap=False,
        max_depth=74,
        max_features="log2",
        min_samples_split=6,
        n_estimators=242,
    )

    # Define the features and target
    features_train, target_train, features_val, target_val = define_features_target(df)

    # Fit the model
    rf.fit(features_train, target_train)

    # Evaluate the model
    target_pred_train = rf.predict(features_train)
    target_pred_val = rf.predict(features_val)

    return rf


def get_predictions(df):

    # Define the model
    model = define_model(df)

    # Data to predict
    data = pd.read_csv(
        "https://storage.googleapis.com/mlsd-project/newData_7Days.csv", sep=";"
    )

    # Save the predictions
    pred = model.predict(data)
    current_dir = os.path.dirname(os.path.realpath(__file__))
    new_csv_path = os.path.join(current_dir, "data/predictions.csv")
    pd.DataFrame(pred).to_csv(new_csv_path, sep=";", index=False)

    # Push on the cloud
    service_account_path = os.path.join(
        current_dir, "level-lyceum-400516-877e79f06a39.json"
    )
    bucket_name = "mlsd-project"
    source_file_path = os.path.join(current_dir, "data/predictions.csv")
    destination_blob_name = "predictions.csv"
    upload_blob(
        service_account_path, bucket_name, source_file_path, destination_blob_name
    )


if __name__ == "__main__":

    df_train = get_data()

    new_df_train = define_training_data(df_train)

    get_predictions(new_df_train)

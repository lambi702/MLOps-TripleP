"""
    updateTrain.py : This code is executed every day to update the model with the new data.
    We must first update the data in the csv file to have them up to date.
    Then we can update the model with the new data.
    Once the model is updated, we can make predictions with the new data.
    The predictions and the new data are then saved on the cloud.
"""

import os
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from define_api_data import define_new_data, get_statistics, get_7days_data,\
      get_training_data, upload_blob

def define_data(d_f):
    """
    Function to define the data and to clean it

    Arguments:
        - d_f: dataframe containing the data
    """

    d_f = d_f.rename(columns={"Unnamed: 0": "Timestamp"})
    d_f["Timestamp"] = pd.to_datetime(d_f["Timestamp"])

    d_f["Month"] = d_f["Timestamp"].dt.month
    d_f["Day"] = d_f["Timestamp"].dt.day
    d_f["Hour"] = d_f["Timestamp"].dt.hour + d_f["Timestamp"].dt.minute / 60

    d_f = d_f.drop(columns=d_f.columns[:9])
    d_f = d_f.drop(columns=d_f.columns[1:10])

    return d_f


def get_data():
    """
    Function to get the date of today and update data accordingly

    """
    # Get access to the training data: no_outliers.csv
    d_f_train_get = pd.read_csv(
        "https://storage.googleapis.com/mlsd-project/no_outliers.csv",
        sep=";",
        index_col=1,
    )

    # New data
    d_f_new = define_new_data(d_f_train_get)
    data = get_statistics(d_f_new)

    # Save the next 7 days data:
    get_7days_data(data)

    # Save the data for training
    get_training_data(data)

    # Dataframe of the training data
    d_f_train_get = define_data(d_f_train_get)

    return d_f_train_get


def define_training_data(d_f_train_old):
    """
    Function to define the training data

    Arguments:
        - d_f_train_old: dataframe containing the training data
    """

    # Get the data for training
    get_training_data(d_f_train_old)

    # Load the new data for training
    current_dir = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(current_dir, "data/newData_forTrain.csv")
    d_f_train_new = pd.read_csv(csv_path, sep=";", index_col=1)

    # Concatenate the two dataframes
    d_f_train_new = pd.concat([d_f_train_old, d_f_train_new])

    return d_f_train_new


def define_features_target(d_f):
    """
    Function to define the features and target of the model

    Arguments:
        - d_f: dataframe containing the data
    """

    target = d_f.drop(columns=d_f.columns[1:])
    features = d_f.drop(columns=["Power_Total"])

    features_train, features_temp, target_train, target_temp = train_test_split(
        features, target, test_size=0.25, random_state=42
    )
    features_val, _, target_val, _ = train_test_split(
        features_temp, target_temp, test_size=0.5, random_state=42
    )

    return features_train, target_train, features_val, target_val


def define_model(d_f):
    """
    Function to define the model

    Arguments:
        - d_f: dataframe containing the data
    """

    # Define the model
    r_f = RandomForestRegressor(
        bootstrap=False,
        max_depth=74,
        max_features="log2",
        min_samples_split=6,
        n_estimators=242,
    )

    # Define the features and target
    features_train, target_train, _, _ = define_features_target(d_f)

    # Fit the model
    r_f.fit(features_train, target_train)

    # Evaluate the model
    #target_pred_train = r_f.predict(features_train)
    #target_pred_val = r_f.predict(features_val)

    return r_f


def get_predictions(d_f):
    """
    Function to get the predictions with the model computed
    
    Arguments:
        - d_f: dataframe containing the data
    """

    # Define the model
    model = define_model(d_f)

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

    d_f_train = get_data()

    new_d_f_train = define_training_data(d_f_train)

    get_predictions(new_d_f_train)

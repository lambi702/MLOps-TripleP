from datetime import datetime 
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import pickle

# MODEL ------

def define_data(df):
    """
    Function to define the data and to clean it

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

def define_features_target(df):
    """
    Function to define the features and target of the model

    Arguments:
        - df: dataframe containing the data
    """

    target = df.drop(columns=df.columns[1:])
    features = df.drop(columns=['Power_Total'])
    
    features_train, features_temp, target_train, target_temp = train_test_split(features, target, test_size=0.25, random_state=42)
    features_val, features_test, target_val, target_test = train_test_split(features_temp, target_temp, test_size=0.5, random_state=42)

    return features_train, target_train, features_val    


def define_model(df):
    """
    Function to define the model

    Arguments:
        - df: dataframe containing the data
    """

    # Define the model
    rf = RandomForestRegressor(bootstrap=False, 
                               max_depth=74, 
                               max_features='log2',
                               min_samples_split=6, 
                               n_estimators=242)
    
    # Define the features and target
    features_train, target_train, features_val = define_features_target(df)
    
    # Fit the model
    rf.fit(features_train, target_train)

    # Save the model
    folder_name = "saved-models"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    model_path = os.path.join(folder_name, "random_forest_model.pkl")

    with open(model_path, 'wb') as file:
        print("Model saved")
        pickle.dump(rf, file)


def convert_date(row):
    """
    Function to convert the date from the csv file to a datetime object: human readable

    Arguments:
        - row: row of the dataframe
    """

    month, day, hour = int(row['Month']), int(row['Day']), row['Hour']
    year = datetime.now().year  

    hour_int = int(hour) 
    minute_dec = (hour % 1) * 60 

    date_string = f"{year}-{month}-{day} {hour_int}:{int(minute_dec)}"
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M')  


def get_predictions():
    """
    Function to get the predictions of the model

    """

    current_dir = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(current_dir, "../data/no_outliers.csv")
    df_train = pd.read_csv(csv_path, sep=';', index_col=1)

    df_train = define_data(df_train)
    
    # Load the model if it exists or create it
    if not os.path.exists('saved-models/random_forest_model.pkl'):
        rf = define_model(df_train)
    
    with open('saved-models/random_forest_model.pkl', 'rb') as file:
        rf = pickle.load(file)
        print("Model loaded")
    

    # Load the predicted meteorological data of the next 7 days
    csv_path = os.path.join(current_dir, "../data/newData_7Days.csv")
    data = pd.read_csv(csv_path, sep=';')

    # Modify the date in the data so that is human readable 
    date = []
    for _, row in data.iterrows():
        date.append(convert_date(row))

    # Get the predictions for the next 7 days
    predictions = rf.predict(data)


    # return what we need in the API
    return predictions, date, data['SWD'], data['SWDtop']



if __name__ == '__main__':
    predictions, date, SWD, ST = get_predictions()

    df = pd.DataFrame({
    'predictions': predictions,
    'days': date,
    'SWD': SWD,
    'ST': ST
    })

    print(df.head())





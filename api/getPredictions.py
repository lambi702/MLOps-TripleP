from datetime import datetime 
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import os

# MODEL ------

def define_data(df):
    
    df = df.rename(columns={'Unnamed: 0': 'Timestamp'})
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    df['Month'] = df['Timestamp'].dt.month
    df['Day'] = df['Timestamp'].dt.day
    df['Hour'] = df['Timestamp'].dt.hour + df['Timestamp'].dt.minute / 60

    df = df.drop(columns=df.columns[:9])
    df = df.drop(columns=df.columns[1:10])

    return df

def define_features_target(df):
    target = df.drop(columns=df.columns[1:])
    features = df.drop(columns=['Power_Total'])
    
    features_train, features_temp, target_train, target_temp = train_test_split(features, target, test_size=0.25, random_state=42)
    features_val, features_test, target_val, target_test = train_test_split(features_temp, target_temp, test_size=0.5, random_state=42)

    return features_train, target_train, features_val    


def define_model(df):

    rf = RandomForestRegressor(bootstrap=False, 
                               max_depth=74, 
                               max_features='log2',
                               min_samples_split=6, 
                               n_estimators=242)
    
    features_train, target_train, features_val = define_features_target(df)
    
    rf.fit(features_train, target_train)
    # target_pred_train = rf.predict(features_train)
    # target_pred_val = rf.predict(features_val)

    return rf

def convert_date(row):
    month, day, hour = int(row['Month']), int(row['Day']), row['Hour']
    year = datetime.now().year  # Utilisation de l'année actuelle

    hour_int = int(hour)  # Partie entière des heures
    minute_dec = (hour % 1) * 60  # Partie décimale des heures, convertie en minutes

    date_string = f"{year}-{month}-{day} {hour_int}:{int(minute_dec)}"
    return datetime.strptime(date_string, '%Y-%m-%d %H:%M')  # Conversion en objet datetime

   


def get_predictions():

    current_dir = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(current_dir, "../data/no_outliers.csv")
    df_train = pd.read_csv(csv_path, sep=';', index_col=1)

    df_train = define_data(df_train)
    rf = define_model(df_train)

    # Load the data and get the predictions
    csv_path = os.path.join(current_dir, "../data/new_data.csv")
    data = pd.read_csv(csv_path, sep=';')

    date = []
    for _, row in data.iterrows():
        date.append(convert_date(row))

    
    predictions = rf.predict(data)

    
    return predictions, date

if __name__ == '__main__':
    predictions = get_predictions()
    print(predictions)



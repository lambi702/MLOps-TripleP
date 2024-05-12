# Daily Model Update Workflow

## Overview
The `updateTrain.py` script automates daily updates and training of our model. This script is scheduled to run at 2:30 AM (UTC time, corresponding to 2:30 AM in Belgium) using GitHub Actions. The automated process ensures that the data for the upcoming seven days is uploaded to the cloud and the model incorporates the most recent data for predictions.

## Process Description

### Data Update
Each day at 2:30 AM, the file `newData_7Days.csv` is uploaded to the cloud with data covering the next seven days. The data from the previous day is added to our training dataset to enhance the model's accuracy.

### Model Training
Once the data is updated, the model is retrained using the newly incorporated data from the previous day. After retraining, the model computes predictions for the next seven days.

### Automation Setup
The process is automated through a GitHub Action named *Daily Update Model*. This action is defined in the `.github/workflows/DailyUpdateModel.yml` file within our main repository. It's crucial to store this file in the main repository directory to ensure the GitHub Action is triggered as scheduled.

### Dependencies
All required dependencies for running `updateTrain.py` are listed in the `dependencies.txt` file, located in the `api` folder of our repository.

## Performance
The entire update and training process takes approximately 1 minute and 30 seconds, making it highly efficient for daily execution.

## Visibility
You can monitor the progress and outcomes of these actions in the *Actions* tab of the GitHub repository.

## Advantages
This setup allows for continuous updating of the data and model without manual intervention, ensuring our application always has access to the latest predictions.


# ML Pipeline Overview

## Data Processing
The ML pipeline begins with data processing, handled by `define_api_data.py`. This script defines functions to clean and convert raw data into a format suitable for modeling. It includes:
- Renaming columns and converting date-time information.
- Calculating statistical metrics like mean and standard deviation to normalize the data.

## Model Training
The model training process involves:
- Defining features and targets from the processed data.
- Using a Random Forest algorithm to train the model with training data.
- Evaluating model performance on validation data.

## Prediction
Once the model is trained, the prediction process is executed, which involves:
- Fetching new data from a predefined source.
- Using the trained model to make predictions on this new data.
- Storing predictions in CSV format and potentially uploading them to a cloud storage.

## Containerization
The application is containerized using Docker, as outlined in the `Dockerfile`. This includes:
- Setting up a Python environment.
- Installing necessary libraries.
- Defining the execution command for the application.

## Update Training
The `updateTrain.py` script updates the training data and recalculates predictions as needed. This is part of maintaining the model's accuracy over time.

---

For further details on contributing to this project or inquiries, refer to the contact section in the main `README.md`.
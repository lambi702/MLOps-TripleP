# Complete ML Pipeline Overview

## Project Introduction
This document provides a detailed overview of the ML pipeline for the MLOps-TripleP project, which predicts solar panel production over university parking areas. Our setup includes data processing, model training, prediction, containerization with Docker, orchestration with Docker Compose, and automated updates using GitHub Actions.

## Data Processing
The ML pipeline starts with data processing implemented in `define_api_data.py`. This script includes functions to clean and reformat the raw data for modeling. Key processes include:
- Renaming columns for clarity.
- Converting timestamps into a more usable format.
- Normalizing data based on computed statistical metrics like mean and standard deviation.

## Model Training
Model training involves:
- Defining features and target variables from the processed data.
- Training a Random Forest model using the training dataset.
- Evaluating the model on validation data to ensure its effectiveness.

## Prediction
Following training, the model is used for predictions:
- New data is fetched from specified sources.
- The trained model predicts based on this new data.
- Predictions are stored in a CSV file and can be uploaded to cloud storage for further use.

## Containerization with Docker
The application is containerized using a Dockerfile which ensures the Python environment is prepared with all dependencies:
- Building an image from `python:3.9-slim`.
- Setting up the necessary directory structure.
- Installing required packages from `requirements.txt`.
- Running the application using Gunicorn as a WSGI server.

## Orchestration with Docker Compose
The Docker Compose configuration automates the deployment of the web service:
```yaml
version: '3'
services:
  web:
    image: appmlsd
    ports:
      - "8080:8080"
    environment:
      - DASH_APP=test.py

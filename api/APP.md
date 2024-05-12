# Development of the Application

## Visualization of the application

The application utilizes the Dash Plotly library to build interactive dashboards for visualizing electricity production predictions. Users can interact with the dashboard through features like zoom, pan, and download. Additionally, a dropdown menu allows users to select the timeframe for predictions displayed on the graph (1, 3, or 7 days).

![Prediction Dashboard](https://github.com/lambi702/MLOps-TripleP/assets/73172824/f6420250-0b24-42ff-8102-8cbfeb4ab9e6)

Meteorological data, which are crucial features for predicting electricity production, are also displayed under the predictions as illustrated in the images below.

![Meteorological Data 1](https://github.com/lambi702/MLOps-TripleP/assets/73172824/bc4dc61e-ce23-40c1-ae07-cfc0afa8f9ef)
![Meteorological Data 2](https://github.com/lambi702/MLOps-TripleP/assets/73172824/96e19842-0df7-4f69-8ba7-6538ddda51f4)

## Data on the Cloud

The data and predictions used in the application are stored in a Google Cloud bucket. This setup ensures fast and easy access to the data and allows for independent updates from the application model. The data is refreshed daily through a GitHub Action, ensuring the application always has the latest information available.

![Cloud Data Management](https://github.com/lambi702/MLOps-TripleP/assets/73172824/ae36c79e-9b47-4907-b271-2a21de7c3974)

## Docker and Google Cloud Deployment

The application's API is packaged into a Docker container, facilitating deployment on Google Cloud. This containerization ensures that the application can be accessed from any machine via a link.

### Docker Configuration

The `Dockerfile` sets up the environment for running our application:

```dockerfile
FROM python:3.9-slim

RUN mkdir -p /api/src /api/data /api/savedModels

WORKDIR /api

# Copy application files
COPY src/test.py ./src/
COPY src/getPredictions.py ./src/
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Set environment variables
ENV DASH_APP=test.py
ENV PORT 8080

# Start the application
CMD exec gunicorn --bind :$PORT src.test:server
```
#### Explanation of Dockerfile Directives

- `FROM python:3.9-slim`:
  Initializes the build stage and sets the base image to `python:3.9-slim`, a lightweight version of the official Python image. This choice helps reduce the overall size of our Docker image while providing the necessary Python environment.

- `RUN mkdir -p /api/src /api/data /api/savedModels`:
  Creates three directories within the Docker container. These directories are designated for storing the application's source code (`src`), data (`data`), and saved machine learning models (`savedModels`). Using `mkdir -p` ensures that the entire path is created if it doesn't already exist.

- `WORKDIR /api`:
  Sets the working directory for the Docker container to `/api`. All subsequent commands (like `COPY` and `RUN`) will be executed relative to this directory.

- `COPY src/test.py ./src/` and `COPY src/getPredictions.py ./src/`:
  Copies the Python scripts `test.py` and `getPredictions.py` from the local `src` directory to the `src` directory in the container. These scripts contain the main logic for the application's dashboard and its predictions functionality.

- `COPY requirements.txt .`:
  Copies the `requirements.txt` file from the local directory to the current working directory (`/api`) in the container. This file lists all the Python packages that the application requires.

- `RUN pip install -r requirements.txt`:
  Installs the Python packages specified in `requirements.txt` using pip. This step is crucial to ensure all dependencies are available in the container, allowing the application to run as expected.

- `ENV DASH_APP=test.py`:
  Sets an environment variable `DASH_APP` within the container, which points to the main dashboard application script. This variable is used to specify which Python file to run when starting the server.

- `ENV PORT 8080`:
  Sets an environment variable `PORT` to `8080`. This variable defines the port number on which the application will listen, making it accessible on this port inside the container.

- `CMD exec gunicorn --bind :$PORT src.test:server`:
  Specifies the command to run by default when the container starts. This command uses Gunicorn, a Python WSGI HTTP server, to serve the Dash application. `--bind :$PORT` binds the server to the port specified by the `PORT` environment variable, and `src.test:server` specifies the application and callable within the `test.py` file that Gunicorn will serve.

This Dockerfile is crafted to ensure that the deployment of our Dash application is reproducible and isolated from external system configurations, providing a consistent environment for both development and production use.


### Docker Compose Setup

To simplify deployment, we use `docker-compose` which orchestrates the Docker container based on the following configuration:

```yaml
version: '3'
services:
  web:
    image: mlsd-app
    ports:
      - "8080:8080"
    environment:
      - DASH_APP=test.py
```

This setup allows our application to run seamlessly on Google Cloud, with the necessary libraries specified in the `requirements.txt` and `dependencies.txt` files for the API and ML pipelines respectively.
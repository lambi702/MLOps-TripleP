FROM python:3.9-slim

RUN mkdir -p /api/src /api/data /api/savedModels

WORKDIR /api

# Copy the current directory contents into the container at /app
COPY src/test.py ./src/
COPY src/getPredictions.py ./src/
#COPY data/  ./data
#COPY savedModels/ ./savedModels
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt


# Define environment variable to tell the container where the app is (i.e. the file to run)
ENV DASH_APP=test.py
ENV PORT 8080

#CMD ["gunicorn", "-b", "0.0.0.0:5000", "src.test:server"]
CMD exec gunicorn --bind :$PORT src.test:server
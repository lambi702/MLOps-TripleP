# Development of the Application

## Visualization of the application

The application uses the library Dash Plotly, which aims to build dashboards with Python.
Our application displays the prediction of the production of electricity 
with the help of a dashboard that is interactive (zoom, plan, download).
This configuration provides a suitable way to visualize the predictions  
easily.
In addition, there is a dropdown that offers the possibility to select the number of
next days that will be shown on the graph for the predictions (1, 3 or 7).

![image](https://github.com/lambi702/MLOps-TripleP/assets/73172824/f6420250-0b24-42ff-8102-8cbfeb4ab9e6)

Under the predictions, we also wanted  to display some of the meteorological data that has been used as a feature to 
predict the production of electricity. Two have been displayed, as shown in the two figures below.

![image](https://github.com/lambi702/MLOps-TripleP/assets/73172824/bc4dc61e-ce23-40c1-ae07-cfc0afa8f9ef)
![image](https://github.com/lambi702/MLOps-TripleP/assets/73172824/96e19842-0df7-4f69-8ba7-6538ddda51f4)


## Data on the Cloud

The predictions and data that are displayed through dashboards in the application 
are stored on the Google Cloud in a bucket to be accessed easily  and quickly. 
It also provides the possibility to update those data independently of the application 
model. The application adapts itself immediately as the data changes. The data are 
updated every day thanks to the Action of GitHub. 

![image](https://github.com/lambi702/MLOps-TripleP/assets/73172824/ae36c79e-9b47-4907-b271-2a21de7c3974)

## Docker and Google Cloud

The API has been packaged in a Docker container with the file *DockerFile*.
This lets us deploy it on the Google Cloud and the application is thus usable thanks to a link with any other machine.
The file *requirements.txt* contains the required libraries for the API, while the *dependencies.txt* file
contains the required libraries for the launch of the ML Pipelines to update the data.




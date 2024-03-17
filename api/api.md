<!-- explain in the read me how to launch the docker app -->

## instruction to build and run the container
Before running the container, you need to go inside the api folder and run the following commands in a terminal:
```bash
docker build -t api .
docker run -p 5000:5000 api
```

## instruction to use the API
Once the container is running, you can use the API by sending a request to the following URL:
```
http://localhost:5000/<date>
```
where `<date>` is the date you want to get the data for. The date should be in the format `YYYY-MM-DD`. For example, to get the data for the 1st of January 2021, you would send a request to:
```
http://localhost:5000/2021-01-01
```
The API will return a JSON object with the data for the specified date.

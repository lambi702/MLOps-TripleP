# Final touches to the code: LINTING

![`pylint` logo](logo.png)

Before submitting the project, we decided to use `pylint` as a linting package to check the code for any errors or warnings. We installed `pylint` using the following command:

```bash
pip install pylint
```

Next, we ran `pylint` on all the files in the project using the following command:

```bash
pylint file_name.py
```

After running `pylint`, we fixed all the errors and warnings in the code. This step ensures that the code is clean and follows the best practices for Python programming. The only warnings left were ones we had not control over and the naming convention of two files on which our cloud relied so we decided to left those as is. Once the code passed the `pylint` checks, we were ready to submit the project.

Almost every file scored 10/10 expect the `api/define_api_data.py`with 8.8/10, `api/updateTrain.py`with 9.82/10, `api/src/test.py` with 8.53/10 (`dash` import error) and `api/src/getPredictions.py` with 9.52/10.
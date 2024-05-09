## Daily Update of the model

Every day at 2h30 am, the data are set up to date so that the file 'newData_7Days.csv' is uploaded on the cloud with the new newt 7 days.
The previous day is added to the training data to train de the model.
Once the data is updated, the model is retrained with the new data from the previous day, and 
the predictions for the next 7 days from today are computed and updated on the cloud to be used by the app.

This schema is done with the file *updateTrain.py*, which uses functions in *define_api_data.py*. 
This file is launched through the GitHub Action capacities. The Action is called the *Daly Update Model*
and all the workflow are visible in the *Actions* tab of this repository.
All the requirements to launch the file are described in the *dependencies.txt* file located in the *api* folder.

The duration of the action is around 1 minute and 30 seconds, which is quite reasonable to train the model 
every day with new data.
As it works on schedule and at the UTC time, the hour fixed for the schedule is 00:30, which corresponds 
to 2h30 am in Belgium.

Thanks to this capacity, the data and the model can be updated every day, and the data can be uploaded to the 
cloud without any manual intervention.

The file that describes the action, *DailyUpdateModel.yml*, is located in the main repository, as the schedule does not work if not.
The path is the following: .github/workflows/DailyUpdateModel.yml

# Prediction Methodology Using Modified Data and Future Forecast ?

The data used to train the models were data collected during the year 2022 
and come from the meteorological institute of the University of Liège. 
The data are collected every 15 minutes and are used to predict the
production of electricity from solar panels.

We managed to get access to future data from the meteorological institute of the University, but without success. 
Therefore, we were not able to predict in real life the production of electricity from solar panels in the API in order to build a 'real-time' prediction model.

That is why we decided to use the modified data from the year 2022 to predict the production of electricity from solar panels. 
In order to build a data set that is as close as possible to the real data, we have modified the data from the year 2022. We have computed the mean and standard deviation of the data, and we have added a random noise to the data for each feature.
We then check the bounds of the data to ensure that the modified data is within the bounds of the real data.
Indeed, these following bounds do apply to the data:
    
    - 'CD' : [0, 1]
    - 'CM' : [0, 1]
    - 'CU' : [0, 1]
    - 'RH2m' : [0, 100]
    - 'SNOW' : [0, ∞[
    - 'SWD' : [0, ∞[
    - 'SWDtop' : [0, ∞[
    - 'WS100m' : [0, ∞[
    - 'WS10m' : [0, ∞[


### Deal with the future data

The idea is to create an API that is as close as possible to a real case scenario: we want to consider that we have meteorological predicitons data
for the next seven days, for example, and we want to predict the production of electricity from solar panels for the next seven days so that we can plan the energy production in the future.

Indeed, in our cases, as we have built a 'false' dataset, we have more than 7 days after the day considered as today in the dataset.
Therefore, the data from this year in the new dataset will be added to the data from 2022 in order to predict the production of electricity from solar panels for the next seven days. 
Data beyond seven days will be progressively added as it becomes available.

The API will utilize meteorological forecasts for the next seven days to predict solar electricity production over the same period, facilitating future energy production planning accordingly. 


 
    

  
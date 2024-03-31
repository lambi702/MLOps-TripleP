from datetime import datetime
from flask import Flask, render_template, request, jsonify
import json
from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
from getPredictions import get_predictions


app = Dash(__name__)



# call the model to get the predictions
pred, date = get_predictions()

# data
df = pd.DataFrame({
    'predictions': pred,
    'days': date,
})

fig = px.line(df, x='days', y='predictions')

today = datetime.now()

app.layout = html.Div([
    html.H1(children='Prediction of Parking Area Solar Panel Electricity Generation at the University of Liège'
            , style={'textAlign':'center'}),
    html.H2(today.strftime('%d-%m-%Y'), style={'textAlign':'center'}),

    # Add some explanantions about the project
    html.H2('Project description:'),
    html.P('This project aims to predict the electricity generation of the solar panels located in the parking area of the University of Liège. The predictions are based on meteorological data such as temperature, humidity and solar irradiance. The data is collected from the meteorological station of the university and is used to train a machine learning model. The model is then used to predict the electricity generation of the solar panels for the next days.'),

    # graph of the predictions of the solar panels
    html.H2('Prediction of the electricity generation of the solar panels for the next days:'),
    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    # Graph of the meteorological data
    html.H2('Meteorological data:'),

])

import plotly.express as px

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
# update the graph based on the dropdown value
def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')



# # Get today's date
# def get_today_date():
#     
#     return today.strftime('%Y-%m-%d')

# # Get predictions for next days
# def get_weather_predictions():
#     pred = [
#         {"date": "2024-04-01", "temperature": 25, "humidity": 70, "solar_irradiance": 800},
#         {"date": "2024-04-02", "temperature": 26, "humidity": 65, "solar_irradiance": 850},
#         {"date": "2024-04-03", "temperature": 24, "humidity": 72, "solar_irradiance": 780}
#     ]
#     return pred




# @app.route('/')
# def upload_file():

#     today_date = get_today_date()

#     to_return = '''
#     <html>
#         <body>
#             <form action = "/uploader" method = "POST" 
#                 enctype = "multipart/form-data">
#                 <input type = "file" name = "file" />
#                 <input type = "submit"/>
#             </form>         
#         </body>
#     </html>
#     '''
#     return f'<h1>Bonjour ! Aujourd\'hui, nous sommes le {today_date}.</h1>'
#     return to_return


# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file_post():
#     if request.method == 'POST':
#         f = request.files['file']
#         data = json.load(f)
#         return jsonify(data)

if __name__ == '__main__':
    app.run(debug = True)#, host='0.0.0.0')
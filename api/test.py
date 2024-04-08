from datetime import datetime
from flask import Flask, render_template, request, jsonify
import json
from dash import Dash, html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px
from getPredictions import get_predictions


app = Dash(__name__)



# call the model to get the predictions
pred, date, swd, swdtop = get_predictions()

today = datetime.now()
# data
df = pd.DataFrame({
    'predictions': pred,
    'days': date,
    'SWD': swd,
    'SWDtop': swdtop
})


fig = px.line(df, x='days', y='predictions', labels={'days':'Date', 'predictions':'Predicted electricity generation (W)'})
fig2 = px.line(df, x='days', y='SWD', labels={'days':'Date', 'SWD':'Horizontal Irradiance (W/m²)'})
fig3 = px.line(df, x='days', y='SWDtop',  labels={'days':'Date', 'SWDtop':'Irradiance top atmosphere (W/m²)'})

app.layout = html.Div([
    html.H1(children='Prediction of Parking Area Solar Panel Electricity Generation at the University of Liège'
            , style={'textAlign':'center'}),
    html.Div(children="""
             A. Birtles, G. Delporte, R. Lambermont and A. Louis
             """
            , style={'textAlign':'center'}),

    html.H2(today.strftime('%d-%m-%Y'), style={'textAlign':'center'}),

    # Add some explanantions about the project
    html.H2('Project description:'),
    html.P('This project aims to predict the electricity generation of the solar panels located in the parking area of the University of Liège. The predictions are based on meteorological data such as temperature, humidity and solar irradiance. The data is collected from the meteorological station of the university and is used to train a machine learning model. The model is then used to predict the electricity generation of the solar panels for the next days.'),

    # graph of the predictions of the solar panels
    html.H2('Prediction of the electricity generation of the solar panels for the next days:'),
    dcc.Dropdown(
        id='display-time',
        options=[
            {'label': '1 day', 'value': 1},
            {'label': '3 days', 'value': 3},
            {'label': '7 days', 'value': 7}
        ],
        value=7  # Par défaut, afficher les données des 7 prochains jours
    ),
    dcc.Graph(
        id='graph_predictions',
        figure=fig
    ),

    # Graph of the meteorological data
    html.H2('Meteorological data:'),
    html.H3('GlobalHorizontal irradiance', style={'textAlign':'center'}),
    dcc.Graph(
            id='example-graph2',
            figure=fig2
        ),

    html.H3('Total Solar Irradiance at the top of the atmosphere', style={'textAlign':'center'}),
    dcc.Graph(
            id='example-graph3',
            figure=fig3
        ),

])

@app.callback(
    Output('graph_predictions', 'figure'),
    [Input('display-time', 'value')]
)

def update_graph(selected_days):

    # Define the date of today at 1h am
    today_1h = datetime(today.year, today.month, today.day, 1, 0)
    data_to_display = df[df['days'] <= today_1h + pd.Timedelta(days=selected_days)]

    return {
        'data': [
            {'x': data_to_display['days'], 'y': data_to_display['predictions'], 'name': 'Predictions'},
        ]
    }


if __name__ == '__main__':
    app.run(debug = True)#, host='0.0.0.0')
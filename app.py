import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import os

import pandas as pd
import flask
import jwt

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, url_base_pathname=os.environ["SAAGIE_BASE_PATH"]+"/")

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['year'].min(),
        max=df['year'].max(),
        value=df['year'].min(),
        marks={str(year): str(year) for year in df['year'].unique()},
        step=None
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year, request=flask.request):
    filtered_df = df[df.year == selected_year]
    a = request.cookies.to_dict()
    print("******************", flush=True)
    print(a, flush=True)
    print("User qui utilise l'app, c'est: ", flush=True)
    print(jwt.decode(a["SAAGIETOKENINTERNE"], options={"verify_signature": False})["preferred_username"])
    print("******************", flush=True)

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

print("Running First run_server")
app.run_server(host='0.0.0.0', debug=True, port=8050)

if __name__ == '__main__':
    print("Running second run_server")
    app.run_server(host='0.0.0.0', debug=True, port=8050)
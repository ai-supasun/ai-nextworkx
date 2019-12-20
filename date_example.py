import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

df = pd.read_csv('clean_data.csv', parse_dates=['Date'])[:2000]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df['Date'].dt.month.min(),
        max=df['Date'].dt.month.max(),
        value=df['Date'].dt.month.min(),
        marks={str(year): str(year) for year in df['Date'].dt.month.unique()},
        step=None
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df['Date'].dt.month == selected_year]
    traces = []
    for i in filtered_df['Item No'].unique():
        df_by_continent = filtered_df[filtered_df['Item No'] == i]
        traces.append(dict(
            x=df_by_continent['sum_price'],
            y=df_by_continent['Quantity'],
            text=df_by_continent['Receipt No'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'log', 'title': 'GDP Per Capita',
                   },
            yaxis={'title': 'Life Expectancy', 'range': [-200, 5000]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
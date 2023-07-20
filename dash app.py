import dash
from dash import dcc, html
import pandas as pd

# Read the data from the CSV file
df = pd.read_csv('filtered_file.csv')

# Convert the "date" column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Filter the DataFrame to include rows after January 15, 2021
sales_after_jan_15 = df[df['date'] > '2021-01-15']

# Check if there is any increase in sales after January 15, 2021
sales_increased = sales_after_jan_15['sales'].diff().gt(0).any()

# Set up the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='line-chart',
            figure={
                'data': [
                    {'x': df['date'], 'y': df['sales'], 'type': 'line', 'name': 'Sales'},
                ],
                'layout': {
                    'title': 'Sales Over Time',
                    'xaxis': {'title': 'Date'},
                    'yaxis': {'title': 'Sales($)'},
                    'shapes': [
                        # Mark the line chart at January 15, 2021
                        {
                            'type': 'line',
                            'x0': '2021-01-15',
                            'x1': '2021-01-15',
                            'y0': df['sales'].min(),
                            'y1': df['sales'].max(),
                            'line': {
                                'color': 'red',
                                'width': 2,
                                'dash': 'dash',
                            },
                        },
                    ],
                }
            }
        )
    ]),
    html.Div([
        html.H2("Sales Increase After January 15, 2021: {}".format(sales_increased)),
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

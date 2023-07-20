import dash
from dash import dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# Read the data from the CSV file
df = pd.read_csv('required_data.csv')

# Convert the "date" column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Set up the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.Div([
        html.H1('Select Region', style={'textAlign': 'left', 'color': 'white'}),
        dcc.RadioItems(
            id='radio-button',
            options=[
                {'label': region, 'value': region} for region in df['region'].unique()
            ],
            value=df['region'].unique()[0],  # Set the default value for the radio button
            labelStyle={'display': 'inline-block', 'margin': '5px'}
        ),
        html.P(id='comparison-result', style={'color': 'white', 'fontSize': '22px', 'fontWeight': 'bold','textAlign':'right'})
    ], style={'background-color': 'lightpink', 'border': '1px solid #ccc', 'padding': '10px', 'border-radius': '5px'}),
    html.Div([
        dcc.Graph(id='line-chart'),
    ]),
])

# Define a callback to update the line chart and the comparison result based on the selected radio button option
@app.callback(
    [Output('line-chart', 'figure'),
     Output('comparison-result', 'children')],
    [Input('radio-button', 'value')]
)
def update_line_chart(selected_region):
    filtered_df = df[df['region'] == selected_region]

    figure = {
        'data': [
            {'x': filtered_df['date'], 'y': filtered_df['sales'], 'type': 'line', 'name': 'Sales'},
        ],
        'layout': {
            'title': f'Sales Over Time in {selected_region}',
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Sales'},
        }
    }

    # Check if there is any increase in sales after January 15, 2021
    sales_after_jan_15 = filtered_df[filtered_df['date'] > '2021-01-15']
    sales_increased = sales_after_jan_15['sales'].diff().gt(0).any()

    comparison_result = "Sales were higher after January 15, 2021." if sales_increased else "Sales were lower after January 15, 2021."

    return figure, comparison_result

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

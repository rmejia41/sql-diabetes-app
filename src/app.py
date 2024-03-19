#Complete sql code and interactive dash app
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Load the analyzed diabetes data
diabetes_analysis_df = pd.read_csv('https://github.com/rmejia41/open_datasets/raw/main/diabetes_indicators_analysis.csv')

# Map state names to their two-letter codes
state_to_code = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'District of Columbia': 'DC',
    'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
    'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
    'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
    'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR',
    'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA',
    'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY',
}

# Convert state names in the DataFrame to their abbreviations
diabetes_analysis_df['State'] = diabetes_analysis_df['State'].map(state_to_code)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Define the layout of the app with custom styling
app.layout = dbc.Container([
    html.H1("Diabetes Indicators by State", style={'font-family': 'Helvetica, Arial, sans-serif', 'text-align': 'center'}),
    dbc.Row([
        dbc.Col(html.Label([
            "Select Year:",
            dcc.Dropdown(
                id='year-dropdown',
                clearable=False,
                value=diabetes_analysis_df['yearend'].min(),
                options=[{'label': year, 'value': year} for year in diabetes_analysis_df['yearend'].unique()],
                style={'width': '100%', 'display': 'inline-block'}  # Adjust this to fit content
            ),
        ]), width=4),  # Adjust the column width as needed and remove the offset
    ]),
    dcc.Graph(id='diabetes-map'),
], fluid=True)

# Define callback to update graph
@app.callback(
    Output('diabetes-map', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_figure(selected_year):
    filtered_df = diabetes_analysis_df[diabetes_analysis_df['yearend'] == selected_year]

    fig = px.choropleth(filtered_df,
                        locations='State',
                        locationmode="USA-states",
                        color='PercentageDiabetesAmongAdults',
                        hover_name='State',
                        hover_data=['TotalRecords', 'DiabetesAmongAdults'],
                        scope="usa",
                        color_continuous_scale=px.colors.sequential.YlOrRd)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

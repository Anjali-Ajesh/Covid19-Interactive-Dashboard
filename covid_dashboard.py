# covid_dashboard.py

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import requests

# --- 1. Fetch and Process Data ---

def fetch_data():
    """Fetches and processes COVID-19 data from the disease.sh API."""
    try:
        # Fetch per-country data
        countries_url = "https://disease.sh/v3/covid-19/countries"
        countries_response = requests.get(countries_url)
        countries_data = countries_response.json()
        
        # Fetch historical global data
        historical_url = "https://disease.sh/v3/covid-19/historical/all?lastdays=all"
        historical_response = requests.get(historical_url)
        historical_data = historical_response.json()

        return countries_data, historical_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None, None

# Load data into pandas DataFrames
countries_data, historical_data = fetch_data()

if countries_data and historical_data:
    # Process country data for the map
    df_countries = pd.DataFrame(countries_data)
    df_countries = df_countries[['country', 'cases', 'countryInfo']]
    # Extract ISO alpha-3 codes for the map
    df_countries['iso_alpha'] = df_countries['countryInfo'].apply(lambda x: x.get('iso3'))

    # Process historical data for the line chart
    df_historical = pd.DataFrame(historical_data['cases'].items(), columns=['Date', 'Cases'])
    df_historical['Date'] = pd.to_datetime(df_historical['Date'])

    # Calculate global totals for summary cards
    global_cases = df_countries['cases'].sum()
    global_deaths = pd.DataFrame(countries_data)['deaths'].sum()
    global_recovered = pd.DataFrame(countries_data)['recovered'].sum()
else:
    # Create empty dataframes if API fails
    df_countries = pd.DataFrame(columns=['country', 'cases', 'iso_alpha'])
    df_historical = pd.DataFrame(columns=['Date', 'Cases'])
    global_cases, global_deaths, global_recovered = 0, 0, 0


# --- 2. Create Visualizations ---

# Choropleth Map
fig_map = px.choropleth(
    df_countries,
    locations="iso_alpha",
    color="cases",
    hover_name="country",
    color_continuous_scale=px.colors.sequential.Plasma,
    title="Confirmed COVID-19 Cases by Country"
)
fig_map.update_layout(
    template='plotly_dark',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)

# Line Chart for Historical Data
fig_line = px.line(
    df_historical,
    x="Date",
    y="Cases",
    title="Global Confirmed Cases Over Time"
)
fig_line.update_layout(
    template='plotly_dark',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
)


# --- 3. Initialize Dash App ---
app = dash.Dash(__name__)
server = app.server

# --- 4. Define App Layout ---
app.layout = html.Div(style={'backgroundColor': '#111111', 'color': '#FFFFFF', 'fontFamily': 'sans-serif'}, children=[
    html.H1(
        children='COVID-19 Global Data Dashboard',
        style={'textAlign': 'center', 'padding': '20px'}
    ),

    # Summary Cards
    html.Div(className='row', children=[
        html.Div(
            children=[
                html.H3('Total Cases', style={'textAlign': 'center'}),
                html.P(f"{global_cases:,}", style={'textAlign': 'center', 'fontSize': 24, 'color': '#f44336'})
            ],
            style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}
        ),
        html.Div(
            children=[
                html.H3('Total Deaths', style={'textAlign': 'center'}),
                html.P(f"{global_deaths:,}", style={'textAlign': 'center', 'fontSize': 24, 'color': '#9C27B0'})
            ],
            style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}
        ),
        html.Div(
            children=[
                html.H3('Total Recovered', style={'textAlign': 'center'}),
                html.P(f"{global_recovered:,}", style={'textAlign': 'center', 'fontSize': 24, 'color': '#4CAF50'})
            ],
            style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}
        )
    ], style={'textAlign': 'center'}),

    # Graphs
    dcc.Graph(
        id='world-map',
        figure=fig_map
    ),
    dcc.Graph(
        id='time-series-chart',
        figure=fig_line
    )
])

# --- 5. Run the App ---
if __name__ == '__main__':
    app.run_server(debug=True)

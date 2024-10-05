import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import ssl
import certifi
import urllib.request

# Load the dataset
url = "https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv"
ssl._create_default_https_context = ssl._create_unverified_context
ssl_context = ssl.create_default_context(cafile=certifi.where())
with urllib.request.urlopen(url, context=ssl_context) as response:
    df = pd.read_csv(response)

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout for the dashboard
app.layout = html.Div([
    html.H1("World GDP Choropleth Map Dashboard"),

    # Choropleth map
    dcc.Graph(id='choropleth-map'),

    # Bar chart
    dcc.Graph(id='bar-chart')
])


# Callback to update choropleth map
@app.callback(
    Output('choropleth-map', 'figure'),
    Input('choropleth-map', 'id')
)
def update_choropleth_map(_):
    # Create choropleth map
    fig = px.choropleth(
        df,
        locations="CODE",
        color="GDP (BILLIONS)",
        hover_name="COUNTRY",
        title="World GDP by Country (in Billions)",
        labels={"GDP (BILLIONS)": "GDP (Billions)"},
        color_continuous_scale=px.colors.sequential.Plasma
    )

    return fig


# Callback to update bar chart based on choropleth click data
@app.callback(
    Output('bar-chart', 'figure'),
    Input('choropleth-map', 'clickData')
)
def update_bar_chart(click_data):
    # Get selected country from click data
    selected_country = click_data['points'][0]['location'] if click_data else None

    # Create bar chart with highlighted country
    bar_fig = go.Figure()
    for _, row in df.iterrows():
        bar_fig.add_trace(go.Bar(
            x=[row['COUNTRY']],
            y=[row['GDP (BILLIONS)']],
            marker_color='red' if row['CODE'] == selected_country else 'blue'
        ))

    bar_fig.update_layout(
        title='GDP by Country',
        xaxis_title='Country',
        yaxis_title='GDP (Billions)',
        yaxis=dict(range=[0, 2000])
    )

    return bar_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
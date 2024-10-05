import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load gender inequality index data (for demonstration purposes using generic data)
gii_url = "https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv"
gii_df = pd.read_csv(gii_url)

# Placeholder climate vulnerability data
climate_vulnerability_data = {
    "ISO_A3": ["USA", "KEN", "IND", "BRA", "CHN"],
    "Risk": [7.5, 8.2, 6.7, 7.0, 8.0]
}
climate_vulnerability_df = pd.DataFrame(climate_vulnerability_data)

# Merge datasets on country codes
df = pd.merge(gii_df, climate_vulnerability_df, left_on="CODE", right_on="ISO_A3", how="inner")

# Filter the data to match the context of gender inequality and climate vulnerability
df['Gender Inequality Index'] = df['GDP (BILLIONS)'] / 100  # Dummy calculation
df['Climate Vulnerability Index'] = df['Risk']

# Streamlit app layout
st.set_page_config(page_title="Gender Equality and Climate Action Dashboard", layout="wide")
st.title("Gender Equality and Climate Action Dashboard")

st.markdown("""
This dashboard showcases the relationship between gender inequality and climate change vulnerability.
Select a country from the dropdown menu to view more detailed data.
""")

# Sidebar for country selection
dropdown_options = df['COUNTRY'].unique()
selected_country = st.sidebar.selectbox("Select a Country", dropdown_options)
filtered_df = df[df['COUNTRY'] == selected_country] if selected_country else df

# Choropleth map to show climate vulnerability
fig = px.choropleth(
    df,
    locations="CODE",
    color="Gender Inequality Index",
    hover_name="COUNTRY",
    title="Gender Inequality Index by Country",
    labels={"Gender Inequality Index": "Gender Inequality Index"},
    color_continuous_scale=px.colors.sequential.Sunset
)
fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0}, geo=dict(showframe=False, showcoastlines=True))
st.plotly_chart(fig, use_container_width=True)

# Time-series analysis for labor hours by women
st.subheader(f"Increasing Labor Hours for Women Over Time - {selected_country}")
years = ['2018', '2019', '2020', '2021', '2022']
labor_hours = [2, 3, 4, 5, 7]  # Placeholder data
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=years,
    y=labor_hours,
    mode='lines+markers',
    name='Labor Hours by Women',
    line=dict(color='#2980B9', width=3),
    marker=dict(size=8)
))
fig.update_layout(
    xaxis={'title': 'Year'},
    yaxis={'title': 'Labor Hours (in millions)'},
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    plot_bgcolor='#F9F9F9'
)
st.plotly_chart(fig, use_container_width=True)

# Bar chart for economic impact
st.subheader(f"Economic Impact by Country - {selected_country}")
bar_fig = px.bar(
    filtered_df,
    x='COUNTRY',
    y='GDP (BILLIONS)',
    title='Economic Impact by Country',
    labels={'GDP (BILLIONS)': 'GDP (Billions)', 'COUNTRY': 'Country'},
    color_discrete_sequence=['red']
)
bar_fig.update_layout(
    yaxis=dict(range=[0, 2000]),
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    plot_bgcolor='#F9F9F9'
)
st.plotly_chart(bar_fig, use_container_width=True)

# Climate Vulnerability Index chart
st.subheader(f"Climate Vulnerability Index by Country - {selected_country}")
vuln_fig = px.bar(
    filtered_df,
    x='COUNTRY',
    y='Climate Vulnerability Index',
    title='Climate Vulnerability Index by Country',
    labels={'Climate Vulnerability Index': 'Climate Vulnerability Index', 'COUNTRY': 'Country'},
    color_discrete_sequence=['green']
)
vuln_fig.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    plot_bgcolor='#F9F9F9'
)
st.plotly_chart(vuln_fig, use_container_width=True)

# Key Performance Indicators (KPIs)
st.sidebar.subheader("Key Performance Indicators")
avg_gii = filtered_df['Gender Inequality Index'].mean()
avg_cvi = filtered_df['Climate Vulnerability Index'].mean()
st.sidebar.metric(label="Average Gender Inequality Index", value=f"{avg_gii:.2f}")
st.sidebar.metric(label="Average Climate Vulnerability Index", value=f"{avg_cvi:.2f}")

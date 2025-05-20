import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="COVID-19 Global Data Tracker",
    page_icon="🦠",
    layout="wide"
)

# Page title and description
st.title("COVID-19 Global Data Tracker")
st.markdown("""
This interactive dashboard visualizes COVID-19 trends across countries using data from Our World in Data.
Select countries and date ranges to explore cases, deaths, and vaccination data.
""")

# Load data
@st.cache_data(ttl=3600)  # Cache data for 1 hour
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df['date'] = pd.to_datetime(df['date'])
    return df

# Show loading message
with st.spinner('Loading COVID-19 data...'):
    df = load_data()

# Get list of all countries
all_countries = sorted(df['location'].unique())

# Sidebar for user inputs
st.sidebar.header("Filter Data")

# Country selection
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=all_countries,
    default=['United States', 'India', 'Brazil', 'United Kingdom', 'Kenya']
)

# Date range selection
min_date = df['date'].min().date()
max_date = df['date'].max().date()

# Default to last 6 months
default_start_date = max_date - timedelta(days=180)

start_date = st.sidebar.date_input("Start Date", default_start_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

# Metric selection
metrics = st.sidebar.multiselect(
    "Select Metrics to Display",
    options=["Total Cases", "New Cases", "Total Deaths", "New Deaths", "Vaccinations", "Death Rate"],
    default=["Total Cases", "Total Deaths", "Vaccinations"]
)

# Filter data based on user selection
filtered_df = df[
    (df['location'].isin(selected_countries)) & 
    (df['date'] >= pd.Timestamp(start_date)) & 
    (df['date'] <= pd.Timestamp(end_date))
].copy()

# Handle missing values
key_metrics = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_vaccinations', 'people_vaccinated']
for metric in key_metrics:
    if metric in filtered_df.columns:
        filtered_df[metric] = filtered_df.groupby('location')[metric].transform(
            lambda x: x.fillna(method='ffill')
        )

# Calculate death rate
filtered_df['death_rate'] = np.where(
    (filtered_df['total_cases'] > 0) & (filtered_df['total_deaths'].notna()),
    filtered_df['total_deaths'] / filtered_df['total_cases'] * 100,
    np.nan
)

# Calculate vaccination rate
filtered_df['vaccination_rate'] = np.where(
    (filtered_df['population'] > 0) & (filtered_df['people_vaccinated'].notna()),
    filtered_df['people_vaccinated'] / filtered_df['population'] * 100,
    np.nan
)

# Display data overview
st.header("Data Overview")
st.write(f"Displaying data for {len(selected_countries)} countries from {start_date} to {end_date}")

# Show latest statistics
if not filtered_df.empty:
    # Get latest data for each country
    latest_data = filtered_df.groupby('location').apply(
        lambda x: x.sort_values('date').iloc[-1]
    ).reset_index(drop=True)
    
    # Create metrics display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cases", f"{latest_data['total_cases'].sum():,.0f}")
    
    with col2:
        st.metric("Total Deaths", f"{latest_data['total_deaths'].sum():,.0f}")
    
    with col3:
        avg_death_rate = latest_data['death_rate'].mean()
        st.metric("Avg Death Rate", f"{avg_death_rate:.2f}%")
    
    with col4:
        if 'vaccination_rate' in latest_data.columns:
            avg_vax_rate = latest_data['vaccination_rate'].mean()
            st.metric("Avg Vaccination Rate", f"{avg_vax_rate:.2f}%")

    # Display latest data table
    st.subheader("Latest Statistics by Country")
    display_cols = ['location', 'total_cases', 'total_deaths', 'death_rate']
    if 'vaccination_rate' in latest_data.columns:
        display_cols.append('vaccination_rate')
    
    st.dataframe(latest_data[display_cols].sort_values('total_cases', ascending=False))

# Create visualizations based on selected metrics
st.header("COVID-19 Trend Analysis")

# Total Cases
if "Total Cases" in metrics:
    st.subheader("Total COVID-19 Cases Over Time")
    
    fig = px.line(
        filtered_df, 
        x='date', 
        y='total_cases', 
        color='location',
        title='Total COVID-19 Cases',
        labels={'total_cases': 'Total Cases', 'date': 'Date', 'location': 'Country'}
    )
    st.plotly_chart(fig, use_container_width=True)

# New Cases (7-day rolling average)
if "New Cases" in metrics:
    st.subheader("New COVID-19 Cases (7-day Rolling Average)")
    
    # Calculate 7-day rolling average
    plot_df = filtered_df.copy()
    plot_df['rolling_new_cases'] = plot_df.groupby('location')['new_cases'].transform(
        lambda x: x.rolling(window=7).mean()
    )
    
    fig = px.line(
        plot_df, 
        x='date', 
        y='rolling_new_cases', 
        color='location',
        title='7-Day Rolling Average of New Cases',
        labels={'rolling_new_cases': 'New Cases (7-day avg)', 'date': 'Date', 'location': 'Country'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Total Deaths
if "Total Deaths" in metrics:
    st.subheader("Total COVID-19 Deaths Over Time")
    
    fig = px.line(
        filtered_df, 
        x='date', 
        y='total_deaths', 
        color='location',
        title='Total COVID-19 Deaths',
        labels={'total_deaths': 'Total Deaths', 'date': 'Date', 'location': 'Country'}
    )
    st.plotly_chart(fig, use_container_width=True)

# New Deaths
if "New Deaths" in metrics:
    st.subheader("New COVID-19 Deaths (7-day Rolling Average)")
    
    # Calculate 7-day rolling average
    plot_df = filtered_df.copy()
    plot_df['rolling_new_deaths'] = plot_df.groupby('location')['new_deaths'].transform(
        lambda x: x.rolling(window=7).mean()
    )
    
    fig = px.line(
        plot_df, 
        x='date', 
        y='rolling_new_deaths', 
        color='location',
        title='7-Day Rolling Average of New Deaths',
        labels={'rolling_new_deaths': 'New Deaths (7-day avg)', 'date': 'Date', 'location': 'Country'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Vaccinations
if "Vaccinations" in metrics:
    st.subheader("COVID-19 Vaccination Progress")
    
    fig = px.line(
        filtered_df, 
        x='date', 
        y='vaccination_rate', 
        color='location',
        title='Population Vaccination Rate (%)',
        labels={'vaccination_rate': 'Population Vaccinated (%)', 'date': 'Date', 'location': 'Country'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Latest vaccination rates bar chart
    st.subheader("Latest Vaccination Rates by Country")
    
    if not latest_data.empty and 'vaccination_rate' in latest_data.columns:
        fig = px.bar(
            latest_data.sort_values('vaccination_rate', ascending=False), 
            x='location', 
            y='vaccination_rate',
            title='Percentage of Population Vaccinated',
            labels={'vaccination_rate': 'Population Vaccinated (%)', 'location': 'Country'}
        )
        st.plotly_chart(fig, use_container_width=True)

# Death Rate
if "Death Rate" in metrics:
    st.subheader("COVID-19 Death Rate Over Time")
    
    fig = px.line(
        filtered_df, 
        x='date', 
        y='death_rate', 
        color='location',
        title='Death Rate (Deaths/Cases %)',
        labels={'death_rate': 'Death Rate (%)', 'date': 'Date', 'location': 'Country'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Optional: Choropleth Map
st.header("Global COVID-19 Impact")
map_metric = st.selectbox(
    "Select metric for global map",
    options=["total_cases_per_million", "total_deaths_per_million", "people_fully_vaccinated_per_hundred"]
)

# Get the latest data for all countries
latest_global_date = df['date'].max()
latest_global_data = df[df['date'] == latest_global_date].copy()

# Create choropleth map
fig = px.choropleth(
    latest_global_data,
    locations="iso_code",
    color=map_metric,
    hover_name="location",
    color_continuous_scale=px.colors.sequential.Plasma,
    title=f"Global COVID-19 Impact: {map_metric.replace('_', ' ').title()}"
)
fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

# Optional: Include hospitalization data if available
st.header("Hospital & ICU Data")
if 'hosp_patients' in df.columns or 'icu_patients' in df.columns:
    hosp_data_available = any(~filtered_df['hosp_patients'].isna()) if 'hosp_patients' in filtered_df.columns else False
    icu_data_available = any(~filtered_df['icu_patients'].isna()) if 'icu_patients' in filtered_df.columns else False
    
    if hosp_data_available or icu_data_available:
        st.subheader("Hospital and ICU Patients Over Time")
        
        # Hospital patients
        if hosp_data_available:
            fig = px.line(
                filtered_df, 
                x='date', 
                y='hosp_patients', 
                color='location',
                title='COVID-19 Hospital Patients',
                labels={'hosp_patients': 'Hospital Patients', 'date': 'Date', 'location': 'Country'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # ICU patients
        if icu_data_available:
            fig = px.line(
                filtered_df, 
                x='date', 
                y='icu_patients', 
                color='location',
                title='COVID-19 ICU Patients',
                labels={'icu_patients': 'ICU Patients', 'date': 'Date', 'location': 'Country'}
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Hospital and ICU data not available for the selected countries and time period.")
else:
    st.info("Hospital and ICU data not available in the dataset.")

# Footer
st.markdown("---")
st.markdown("""
**COVID-19 Global Data Tracker** | Data source: [Our World in Data](https://ourworldindata.org/coronavirus)  
Last updated: {}
""".format(datetime.now().strftime("%Y-%m-%d")))

# How to run instructions
st.sidebar.markdown("---")
st.sidebar.subheader("How to Run This Dashboard")
st.sidebar.code("streamlit run covid_dashboard.py")
st.sidebar.markdown("Install Streamlit: `pip install streamlit`")






























































































































































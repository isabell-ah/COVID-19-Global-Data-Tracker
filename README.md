# COVID-19 Global Data Tracker

A comprehensive data analysis project that tracks and visualizes global COVID-19 trends using the Our World in Data dataset.

## Project Overview

This project analyzes COVID-19 data across multiple countries, focusing on cases, deaths, and vaccination trends. The analysis includes data cleaning, exploratory data analysis, visualizations, and key insights.

### Key Features

- Data loading and cleaning from Our World in Data COVID-19 dataset
- Time trend analysis for cases, deaths, and vaccinations
- Country comparisons (United States, India, Brazil, United Kingdom, Kenya)
- Multiple visualization types (line charts, bar charts, heatmaps)
- Optional choropleth maps for global data visualization
- Comprehensive insights and findings

## Getting Started

### Prerequisites

The project requires the following Python packages:

- pandas
- matplotlib
- seaborn
- numpy
- plotly (optional, for choropleth maps)

Install the required packages using:

```bash
pip install pandas matplotlib seaborn numpy plotly
```

### Running the Project

The analysis can be run in two ways:

1. **Jupyter Notebook**: Open `covid_data_tracker.ipynb` in Jupyter Notebook or JupyterLab
2. **Python Script**: Run `covid_tracker.py` in your terminal or IDE

## Project Structure

The analysis follows these key steps:

### 1. Data Collection and Loading

We load the COVID-19 dataset from Our World in Data, which provides comprehensive global statistics:

```python
# Load dataset
url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = pd.read_csv(url)
```

The dataset includes daily updates on cases, deaths, testing, and vaccinations for countries worldwide.

### 2. Data Cleaning and Preparation

We prepare the data by:

- Converting dates to datetime format
- Filtering for countries of interest
- Handling missing values
- Calculating derived metrics like death rates

```python
# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Select countries of interest
countries = ['United States', 'India', 'Brazil', 'United Kingdom', 'Kenya']
filtered_df = df[df['location'].isin(countries)]

# Calculate death rate
filtered_df['death_rate'] = np.where(
    (filtered_df['total_cases'] > 0) & (filtered_df['total_deaths'].notna()),
    filtered_df['total_deaths'] / filtered_df['total_cases'] * 100,
    np.nan
)
```

### 3. Exploratory Data Analysis

We analyze trends in cases and deaths over time:

```python
# Plot total cases over time for selected countries
plt.figure(figsize=(14, 8))
for country in countries:
    country_data = filtered_df[filtered_df['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)

plt.title('Total COVID-19 Cases Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Cases', fontsize=12)
plt.legend()
```

### 4. Vaccination Analysis

We track vaccination progress across countries:

```python
# Plot vaccination progress
plt.figure(figsize=(14, 8))
for country in countries:
    country_data = filtered_df[filtered_df['location'] == country]
    plt.plot(country_data['date'], country_data['total_vaccinations'], label=country)

plt.title('COVID-19 Vaccination Progress', fontsize=16)
```

### 5. Advanced Analysis

We perform more detailed analysis including:

- Death rates comparison
- 7-day rolling averages of new cases
- Correlation analysis between metrics

### 6. Choropleth Maps (Optional)

For global visualization, we create choropleth maps showing cases and vaccination rates:

```python
# Create choropleth map of total cases
fig = px.choropleth(
    latest_global_data,
    locations="iso_code",
    color="total_cases_per_million",
    hover_name="location",
    color_continuous_scale=px.colors.sequential.Plasma,
    title="COVID-19 Cases per Million Population"
)
```

## Key Insights

The analysis reveals several important findings:

1. **Case Distribution**: The United States and India have recorded the highest number of total cases among the selected countries, reflecting their large populations and extensive testing.

2. **Death Rates**: Death rates have generally declined over time in most countries, likely due to improved treatment protocols, increased testing, and vaccination of vulnerable populations.

3. **Vaccination Disparities**: Higher-income countries like the United Kingdom and United States achieved faster and more extensive vaccination coverage compared to lower-income countries like Kenya, highlighting global inequities in vaccine access.

4. **Wave Patterns**: Countries experienced distinct waves of infection at different times, with India showing a particularly severe wave in 2021.

5. **Recovery Trends**: Countries show different patterns of recovery and subsequent waves, highlighting the importance of sustained public health measures.

## Visualizations

The project generates several visualizations:

- Line charts tracking cases, deaths, and vaccinations over time
- Bar charts comparing metrics across countries
- Heatmaps showing correlation between different COVID-19 metrics
- Optional choropleth maps displaying global data

## Future Enhancements

Potential improvements to the project:

- Interactive dashboard using Streamlit or Dash
- User input for selecting countries and date ranges
- Inclusion of hospitalization and ICU data
- Predictive modeling for future trends
- Policy analysis correlating government actions with case trends

## Acknowledgments

- Data provided by Our World in Data
- Analysis inspired by global efforts to understand and combat the COVID-19 pandemic
  The dashboard will open in your default web browser at http://localhost:8501

## Stretch Goal Implementation: Interactive Dashboard with Streamlit

Instructions for Running the Interactive Dashboard
To run the interactive Streamlit dashboard:

### 1. Install Streamlit:

pip install streamlit

### 2. Run the dashboard:

streamlit run covid_dashboard.py

### 3.

The dashboard will open in your default web browser at http://localhost:8501

## Key Features of the Implementation

1.  Comprehensive Data Analysis:
    Data loading and cleaning from Our World in Data
    Time trend analysis for cases, deaths, and vaccinations
    Country comparisons with multiple visualization types
2.  Well-Documented Jupyter Notebook:
    Clear narrative explanations between code sections
    Insights and observations for each visualization
    Reproducible code with proper error handling
    \*\*Interactive Dashboard

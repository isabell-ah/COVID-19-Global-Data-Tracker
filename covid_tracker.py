import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Set pandas display options
pd.set_option('display.max_columns', None)

# Load the dataset
url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
df = pd.read_csv(url)

# Display basic information
print(f"Dataset shape: {df.shape}")
print("\nFirst 5 rows:")
print(df.head())
print("\nColumns:")
print(df.columns.tolist())
print("\nMissing values:")
print(df.isnull().sum().sort_values(ascending=False)[:10])  # Top 10 columns with missing values

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Select countries of interest
countries = ['United States', 'India', 'Brazil', 'United Kingdom', 'Kenya']
filtered_df = df[df['location'].isin(countries)]

# Create a copy to avoid SettingWithCopyWarning
filtered_df = filtered_df.copy()

# Handle missing values for key metrics
key_metrics = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_vaccinations']
for metric in key_metrics:
    if metric in filtered_df.columns:
        # Group by country and forward fill missing values
        filtered_df[metric] = filtered_df.groupby('location')[metric].transform(
            lambda x: x.fillna(method='ffill')
        )

# Calculate death rate where data is available
filtered_df['death_rate'] = np.where(
    (filtered_df['total_cases'] > 0) & (filtered_df['total_deaths'].notna()),
    filtered_df['total_deaths'] / filtered_df['total_cases'] * 100,
    np.nan
)

# Set plot style
sns.set(style="darkgrid")
plt.figure(figsize=(14, 8))

# Plot total cases over time for selected countries
plt.figure(figsize=(14, 8))
for country in countries:
    country_data = filtered_df[filtered_df['location'] == country]
    plt.plot(country_data['date'], country_data['total_cases'], label=country)

plt.title('Total COVID-19 Cases Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Cases', fontsize=12)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('total_cases_over_time.png')
plt.show()

# Plot total deaths over time
plt.figure(figsize=(14, 8))
for country in countries:
    country_data = filtered_df[filtered_df['location'] == country]
    plt.plot(country_data['date'], country_data['total_deaths'], label=country)

plt.title('Total COVID-19 Deaths Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Deaths', fontsize=12)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('total_deaths_over_time.png')
plt.show()

# Plot vaccination progress
plt.figure(figsize=(14, 8))
for country in countries:
    country_data = filtered_df[filtered_df['location'] == country]
    plt.plot(country_data['date'], country_data['total_vaccinations'], label=country)

plt.title('COVID-19 Vaccination Progress', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Vaccinations', fontsize=12)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('vaccination_progress.png')
plt.show()

# Compare vaccination rates (people fully vaccinated per hundred)
# Get the latest data for each country
latest_data = filtered_df.groupby('location').apply(
    lambda x: x.sort_values('date').iloc[-1]
).reset_index(drop=True)

plt.figure(figsize=(12, 6))
sns.barplot(x='location', y='people_fully_vaccinated_per_hundred', data=latest_data)
plt.title('Percentage of Population Fully Vaccinated', fontsize=16)
plt.xlabel('Country', fontsize=12)
plt.ylabel('People Fully Vaccinated per 100', fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('vaccination_rates.png')
plt.show()

# Compare death rates
plt.figure(figsize=(14, 8))
for country in countries:
    country_data = filtered_df[filtered_df['location'] == country]
    plt.plot(country_data['date'], country_data['death_rate'], label=country)

plt.title('COVID-19 Death Rate Over Time (Deaths/Cases %)', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Death Rate (%)', fontsize=12)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('death_rate_over_time.png')
plt.show()

# Compare daily new cases (7-day rolling average for smoothing)
plt.figure(figsize=(14, 8))
for country in countries:
    country_data = filtered_df[filtered_df['location'] == country]
    # Calculate 7-day rolling average
    rolling_avg = country_data['new_cases'].rolling(window=7).mean()
    plt.plot(country_data['date'], rolling_avg, label=country)

plt.title('7-Day Rolling Average of New COVID-19 Cases', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('New Cases (7-day avg)', fontsize=12)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('new_cases_rolling_avg.png')
plt.show()

# Generate insights
print("\n=== COVID-19 Data Analysis Insights ===\n")

# 1. Highest case counts
latest_data = latest_data.sort_values('total_cases', ascending=False)
print(f"Countries with highest total cases:")
for i, (idx, row) in enumerate(latest_data.iterrows(), 1):
    print(f"{i}. {row['location']}: {row['total_cases']:,.0f} cases")

# 2. Highest death rates
latest_data = latest_data.sort_values('death_rate', ascending=False)
print(f"\nCountries with highest death rates:")
for i, (idx, row) in enumerate(latest_data.iterrows(), 1):
    print(f"{i}. {row['location']}: {row['death_rate']:.2f}%")

# 3. Vaccination progress
latest_data = latest_data.sort_values('people_fully_vaccinated_per_hundred', ascending=False)
print(f"\nVaccination progress (% fully vaccinated):")
for i, (idx, row) in enumerate(latest_data.iterrows(), 1):
    if pd.notna(row['people_fully_vaccinated_per_hundred']):
        print(f"{i}. {row['location']}: {row['people_fully_vaccinated_per_hundred']:.2f}%")
    else:
        print(f"{i}. {row['location']}: Data not available")

# 4. Case growth rate (last 30 days)
print("\nCase growth in the last 30 days:")
for country in countries:
    country_data = filtered_df[filtered_df['location'] == country].sort_values('date')
    if len(country_data) >= 30:
        current = country_data.iloc[-1]['total_cases']
        month_ago = country_data.iloc[-30]['total_cases']
        growth = ((current - month_ago) / month_ago * 100) if month_ago > 0 else 0
        print(f"{country}: {growth:.2f}% increase")

# Optional: Create a choropleth map of cases or vaccinations
try:
    import plotly.express as px
    
    # Get the latest data for all countries
    latest_date = df['date'].max()
    latest_global_data = df[df['date'] == latest_date].copy()
    
    # Create choropleth map of total cases
    fig = px.choropleth(
        latest_global_data,
        locations="iso_code",
        color="total_cases_per_million",
        hover_name="location",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="COVID-19 Cases per Million Population"
    )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    fig.write_html("covid_cases_map.html")
    
    # Create choropleth map of vaccination rates
    fig = px.choropleth(
        latest_global_data,
        locations="iso_code",
        color="people_fully_vaccinated_per_hundred",
        hover_name="location",
        color_continuous_scale=px.colors.sequential.Viridis,
        title="COVID-19 Vaccination Rates (% Fully Vaccinated)"
    )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    fig.write_html("covid_vaccination_map.html")
    
    print("Choropleth maps created successfully!")
except ImportError:
    print("Plotly not installed. Skipping choropleth maps.")

# Save a summary report
with open('covid19_analysis_summary.txt', 'w') as f:
    f.write("COVID-19 Global Data Tracker - Analysis Summary\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d')}\n")
    f.write(f"Data Source: Our World in Data (up to {latest_date.strftime('%Y-%m-%d')})\n\n")
    
    f.write("Key Insights:\n")
    f.write("1. Case Distribution: ")
    top_country = latest_data.iloc[0]['location']
    f.write(f"{top_country} has the highest number of reported cases among analyzed countries.\n")
    
    f.write("2. Death Rates: ")
    highest_dr_country = latest_data.sort_values('death_rate', ascending=False).iloc[0]['location']
    highest_dr = latest_data.sort_values('death_rate', ascending=False).iloc[0]['death_rate']
    f.write(f"{highest_dr_country} shows the highest death rate at {highest_dr:.2f}%.\n")
    
    f.write("3. Vaccination Progress: ")
    highest_vax = latest_data.sort_values('people_fully_vaccinated_per_hundred', ascending=False).iloc[0]
    f.write(f"{highest_vax['location']} leads in vaccination with {highest_vax['people_fully_vaccinated_per_hundred']:.2f}% fully vaccinated.\n")
    
    f.write("\nAnalyzed Countries: " + ", ".join(countries) + "\n")
    
    f.write("\nGenerated visualizations saved as PNG files in the working directory.\n")
    if 'plotly' in globals():
        f.write("Interactive maps saved as HTML files.\n")

print("\nAnalysis complete! Summary saved to 'covid19_analysis_summary.txt'")






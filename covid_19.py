# Exploratory data analysis
import pandas as pd
import matplotlib.pyplot as plt

def raw_data(base_url):
    confirmed_cases_data_url = base_url + 'time_series_covid19_confirmed_global.csv'
    death_cases_data_url = base_url + 'time_series_covid19_deaths_global.csv'
    recovery_cases_data_url = base_url + 'time_series_covid19_recovered_global.csv'
    # Import datasets as pandas dataframes
    raw_data_confirmed = pd.read_csv(confirmed_cases_data_url)
    raw_data_deaths = pd.read_csv(death_cases_data_url)
    raw_data_recovered = pd.read_csv(recovery_cases_data_url)
    return raw_data_confirmed, raw_data_deaths, raw_data_recovered

# Function for grouping countries by region
def group_by_country(raw_data):
    """Returns data for countries indexed by date"""
    # Group by
    _data = raw_data.groupby(['Country/Region']).sum().drop(['Lat', 'Long'], axis=1)
    # Transpose
    _data = _data.transpose()
    # Set index as DateTimeIndex
    datetime_index = pd.DatetimeIndex(_data.index)
    _data.set_index(datetime_index, inplace=True)
    return _data

# Function to align growth curves
def align_curves(_data, min_val):
    """Align growth curves  to start on the day when the number of known deaths = min_val"""
    # Loop over columns & set values < min_val to None
    for col in _data.columns:
        _data.loc[(_data[col] < min_val), col] = None
    # Drop columns with all NaNs
    _data.dropna(axis=1, how='all', inplace=True)
    # Reset index, drop date
    _data = _data.reset_index().drop(['index'], axis=1)
    # Shift each column to begin with first valid index
    # for col in _data.columns:
    #     _data[col] = _data[col].shift(-_data[col].first_valid_index())
    # shift using lambda function
    _data = _data.apply(lambda x: x.shift(-x.first_valid_index()))
    return _data

# Function to plot time series
def plot_time_series(df, plot_title, x_label, y_label, logy=False, fname='default'):
    """Plot time series and make looks a bit nice"""
    ax = df.plot(figsize=(20, 10), linewidth=2, marker='.', fontsize=20, logy=logy)
    ax.legend(ncol=3, loc='lower right')
    plt.xlabel(x_label, fontsize=20)
    plt.ylabel(y_label, fontsize=20)
    plt.title(plot_title, fontsize=20)
    plt.savefig(fname)
    plt.show()

# Data URL
base_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
countries = ['China', 'US', 'Italy', 'Spain', 'United Kingdom', 'Mexico']
# countries = ['Netherlands', 'Canada', 'Turkey', 'Sweden', 'Mexico', 'Switzerland']
# countries = ['Brazil', 'Mexico', 'Ecuador', 'Peru', 'Colombia', 'Chile']

raw_data_confirmed, raw_data_deaths, raw_data_recovered = raw_data(base_url)
# print(raw_data_confirmed.describe, '\n')
# print(raw_data_deaths.describe, '\n')
# print(raw_data_recovered.describe, '\n')

# Group by country
confirmed_cases_country = group_by_country(raw_data_confirmed)
reported_deaths_country = group_by_country(raw_data_deaths)
recovered_cases_country = group_by_country(raw_data_recovered)

# Align curves
confirmed_country_drop = align_curves(confirmed_cases_country, min_val=25)
deaths_country_drop = align_curves(reported_deaths_country, min_val=25)
recovered_country_drop = align_curves(recovered_cases_country, min_val=25)

# Plotting time series
# Confirmed cases
plot_time_series(confirmed_country_drop[countries], 'Number of Confirmed Cases', 'Days', 'Confirmed Cases by Country', fname='confirmed_cases')
plot_time_series(confirmed_country_drop[countries], 'Number of Confirmed Cases Logarithmic', 'Days', 'Confirmed Cases by Country', logy=True, fname='confirmed_cases_logarithmic')
# Reported deaths
plot_time_series(deaths_country_drop[countries], 'Number of Reported Deaths', 'Days', 'Reported Deaths by Country', fname='reported_deaths')
plot_time_series(deaths_country_drop[countries], 'Number of Reported Deaths Logarithmic', 'Days', 'Reported Deaths by Country', logy=True, fname='reported_deaths_logarithmic')
# Recovered cases
plot_time_series(recovered_country_drop[countries], 'Number of Recovered Cases', 'Days', 'Recovered Cases by Country', fname='recovered_cases')
plot_time_series(recovered_country_drop[countries], 'Number of Recovered Cases Logarithmic', 'Days', 'Recovered Cases by Country', logy=True, fname='recovered_cases_logarithmic')

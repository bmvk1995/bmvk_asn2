import requests
import matplotlib.pyplot as plot
import pandas as bmvk
import numpy as kumar
from scipy.stats import skew

# World_Bank_API endpoint for GDP_Per_Capita data ::
gdp_api_url = 'http://api.worldbank.org/v2/country/{}/indicator/NY.GDP.PCAP.CD?date=2010:2020&format=json'
# World_Bank_API endpoint for CO2_Emissions data
co2_api_url = 'http://api.worldbank.org/v2/country/{}/indicator/EN.ATM.CO2E.KT?date=2010:2020&format=json'
countries = ['USA', 'GBR', 'FRA', 'JPN', 'CAN', 'CHN', 'IND', 'PAK']
# Define indicators and years to retrieve data for Urban Population ::
url = 'http://api.worldbank.org/v2/country'
# Modified to include only 5 countries in Urban Population ::
selected_countries = ['USA', 'CAN', 'GBR', 'FRA', 'CHN']
indicator_code = 'SP.URB.TOTL'  # incdicator for urban population ::
start_year = 1990  # starting year for urban population ::
end_year = 2020  # end year for urban population ::
specific_country = "CHN"  # only country for .describe() function ::
indicator_code = "SP.URB.TOTL.IN.ZS"  # indicator for USA ::

def Fetching_Data(countries, api_url):
    """Fetches the data from World_Bank_API for the given country codes and API endpoint URL and Returns
       a dictionary where keys are country codes and values are lists of data values for each year (2016-2020)"""
    data = {}
    for code in countries:
        url = api_url.format(code)
        response = requests.get(url)
        if response.status_code == 200:
            # Extract data from response JSON ::
            values = [float(d['value']) if d['value']is not None else None for d in response.json()[1]]
            data[code] = values
        else:print(f"Failed to fetch the data forthe {code}")
    return data

def Fetching_Data_Scatter_Plt(selected_countries,indicator_code,start_year,end_year):
    """Fetches data from the World_Bank_API for the Scatter plot"""
    url = 'http://api.worldbank.org/v2/country'
    query_url = f'{url}/{selected_countries}/indicator/{indicator_code}?format=json&date={start_year}:{end_year}'
    response = requests.get(query_url)
    data = response.json()[1]
    return bmvk.DataFrame(data)

def bar_Graph(countries, data, title, y_label):
    """To Create a bar graph of data for given country codes and data and Returns the transposed dataframe"""
    # To Create a DataFrame to hold the data ::
    df = bmvk.DataFrame(data, index=range(2010, 2021))
    # Transpose the DataFrame so that countries are columns ::
    df = df.transpose()
    # Set the plot size ::
    fig, ax = plot.subplots(figsize=(11, 6))
    # Plot the DataFrame as a bar chart ::
    df.plot(kind='bar', alpha=0.8, width=0.8, ax=ax)
    # Set chart title and axis labels ::
    ax.set_title(title, fontsize=15)
    ax.set_xlabel('~~~Country_Names~~~', fontsize=15)
    ax.set_ylabel(y_label, fontsize=15)
    plot.yticks(fontsize=15)
    # Set country codes as x tick labels ::
    ax.set_xticklabels(countries, rotation=0, fontsize=15)
    # Set legend font size ::
    ax.legend(fontsize=15)
    # Show the chart ::
    plot.show()
    # Return the transposed dataframe ::
    return df.transpose()

def Forest_Scatter_plt(countries):
    """Plots for the forest area  and data on a scatter plot"""
    indicator_code = 'AG.LND.FRST.K2'
    start_year = '1990'
    end_year = '2020'
    frequency = 5
    fig, ax = plot.subplots()
    for country in countries:
        data = Fetching_Data_Scatter_Plt(country, indicator_code, start_year, end_year)
        data = data[data.value.notna()]
        data['year'] = bmvk.to_datetime(data.date).dt.year
        data = data.groupby(['year'])['value'].mean().reset_index()
        label = f'{country}'
        ax.plot(data['year'], data['value'], linestyle='--', label=label)
    ax.set_xlabel('~~~Year~~~')
    ax.set_ylabel('!!Forest_Area (Sq_Kms)!!')
    ax.set_title('~~Forest_Area for the Selected Countries~~')
    ax.legend(bbox_to_anchor=(1, 0.5), loc='upper left')
    # Set x-axis ticks
    x_ticks = range(int(start_year), int(end_year) + 1, frequency)
    ax.set_xticks(x_ticks)
    plot.show()

def Arable_Scatter_plt(countries):
    """Plots arable land area data on a scatter plot"""
    indicator_code = 'AG.LND.ARBL.HA'
    start_year = '1990'
    end_year = '2020'
    frequency = 5
    fig, ax = plot.subplots()
    for country in countries:
        data = Fetching_Data_Scatter_Plt(country, indicator_code, start_year, end_year)
        data = data[data.value.notna()]
        data['year'] = bmvk.to_datetime(data.date).dt.year
        data = data.groupby(['year'])['value'].mean().reset_index()
        label = f'{country}'
        ax.plot(data['year'], data['value'], linestyle='--', label=label)
    ax.set_xlabel('Year')
    ax.set_ylabel('~~~Arable Land Area in Hectors~~~')
    ax.set_title('~~~Arable Land Area for the Selected Countries~~~')
    ax.legend(bbox_to_anchor=(1, 0.5), loc='upper left')
    # Set x-axis ticks ::
    x_ticks = range(int(start_year), int(end_year) + 1, frequency)
    ax.set_xticks(x_ticks)
    plot.show()

def Corr_Heat_Map(data, title):
    """To Create a correlation heatmap for the given data"""
    # To Create a DataFrame to hold the data ::
    df = bmvk.DataFrame(data)
    # Compute the correlation matrix ::
    corr_matrix = df.corr()
    # To Create a heatmap
    fig, ax = plot.subplots()
    heatmap = ax.matshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
    # Set chart title and axis labels ::
    plot.title(title)
    plot.xlabel('~~~Country_Codes~~~')
    plot.ylabel('~~~Country_Codes~~~')
    # Set x and y tick labels ::
    ax.set_xticks(kumar.arange(len(df.columns)))
    ax.set_yticks(kumar.arange(len(df.columns)))
    ax.set_xticklabels(df.columns)
    ax.set_yticklabels(df.columns)
    # Add colorbar ::
    fig.colorbar(heatmap)
    # Show the chart ::
    plot.title('~~~China~~~')
    plot.show()

def dataframe():
    """This Function will returns two dataframes one with years as columns and another with countries as columns"""
    # To Create a pandas dataframe from the API data
    df = bmvk.DataFrame(columns=selected_countries,index=range(start_year + 1,end_year))
    # Fill in the dataframe with the data for each country and year
    for code in selected_countries:
        query_url = f'{url}/{code}/indicator/{indicator_code}?format=json&date={start_year}:{end_year}'
        response = requests.get(query_url)
        data = response.json()[1]
        for i in range(len(data)):
            year = int(data[i]['date'])
            value = data[i]['value']
            if value is None:value = 'No data'
            else:value = float(value)
            df.loc[year, code] = value
    # Transpose the dataframe ::
    df_transposed = df.transpose()
    # Clean the transposed dataframe by resetting the index and renaming the columns
    df_transposed = df_transposed.reset_index().rename(
        columns={'index': 'Country'})
    # Only keep data for every 5 years ::
    df_transposed_cleaned = df_transposed[df_transposed.columns[::5]]
    # To Create a pandas dataframe from the API data ::
    df = bmvk.DataFrame(columns=range(start_year + 5,end_year),index=selected_countries)
    # Fill in the dataframe with the data for each country and year ::
    for code in selected_countries:
        query_url = f'{url}/{code}/indicator/{indicator_code}?format=json&date={start_year}:{end_year}'
        response = requests.get(query_url)
        data = response.json()[1]
        for i in range(len(data)):year = int(data[i]['date'])
        value = data[i]['value']
        if value is None:value = 'No data'
        else: value = float(value)
        df.loc[code, year] = value
    # Clean the dataframe by dropping columns that don't fall on a 5-year interval ::
    df_cleaned = df[df.columns[::5]]
    # Transpose the dataframe ::
    df_transposed = df_cleaned.transpose()
    return df_transposed_cleaned, df_transposed

def Method_Describe(specific_country, indicator_code):
    """This function explore the data with .describe() method and to produce the statistical properties for a few indicators"""
    # Set up the URL for the API request
    url = "http://api.worldbank.org/v2/country/{}/indicator/{}?format=json".format(
        specific_country, indicator_code)
    # Send a GET request to the API endpoint ::
    response = requests.get(url)
    # Check if the request was successful ::
    if response.status_code == 200:
        # Extract the data from the response JSON object ::
        data = response.json()[1]
        # To Create a DataFrame from the data ::
        df = bmvk.DataFrame(data)
        # Rename the columns to something more readable ::
        df = df.rename(columns={"date": "Year", "value": "Indicator Value"})
        # Set the index to be the year ::
        df = df.set_index("Year")
        # Generate descriptive statistics for the indicator data ::
        stats = df["Indicator Value"].describe()
        # Calculate skewness of the indicator data ::
        skewness = skew(df["Indicator Value"])
        # Add skewness to the statistics DataFrame ::
        stats["skewness"] = skewness
        return stats
    else: 
        print("Error: XXXXX!! Could not retrieve the data from the World_Bank_API !!XXXXX")
        return None

if __name__ == '__main__':
    # ToFetch GDP_Per_Capita data for each country ::
    gdp_data = Fetching_Data(countries, gdp_api_url)
    # To Create bar graph for GDP_Per_Capita data, get the transposed_dataframe ::
    gdp_df = bar_Graph(countries,gdp_data,'###~~GDP_Per_Capita (2010-2020)~~###','###~~GDP_Per_Capita (Current US $)~~~###')
    # Fetch CO2_Emissions data for each country ::
    co2_data = Fetching_Data(countries, co2_api_url)
    # To Create bar graph for CO2_Emissions data and get the transposed_data_frame :
    co2_df = bar_Graph(countries,co2_data,'###~~CO2_Emissions (2010-2020)~~###','###~~CO2_Emissions(kt)~~###')
    indicators = {'SP.URB.TOTL.IN.ZS': 'Urban Population','NY.GDP.MKTP.KD.ZG': 'GDP Growth','EN.ATM.CO2E.KT': 'CO2_Emissions'}
    # To Create a correlation heatmap of GDP per_capita and CO2_Emissions data ::
    data = {**gdp_data, **co2_data}
    Corr_Heat_Map(data,'Correlation between GDP_Per_Capita and CO2_Emissions for selected countries (2010-2020)')
    Forest_Scatter_plt(countries)
    Arable_Scatter_plt(countries)
    df_transposed_cleaned, df_transposed = dataframe()
    print("\n ~~~~ The Frist Data_Frame for the URBAN_POPULATION ::\n")
    print(dataframe())
    stats = Method_Describe(specific_country, indicator_code)
    print("\n ~~~~ The Stattics for CHINA ::\n")
    print(stats)
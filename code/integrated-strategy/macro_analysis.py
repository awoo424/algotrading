import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys

sys.path.append("..")
mpl.use('tkagg')  # issues with Big Sur

# input: @df, stock tick df
# output: s_gdp, s_unemploy, s_property
def GetSensitivity(price_df):
    # Stock price dataframe pre-processing
    price_df = price_df.reset_index(level='Date')
    price_dates = price_df['Date'].tolist()
    #print(price_df.head())

    # load GDP data
    gdp_df = pd.read_csv('../../database_real/macroeconomic_data/determinants/quarterly_gdp.csv', header=0)
    
    gdp_df['Date'] = pd.to_datetime(gdp_df['Date'])
    gdp_dates = gdp_df['Date'].tolist()
    gdp_values = gdp_df['GDP_current_market_prices'].tolist()
    gdp_counter = 0

    # merge dataframes by adding GDP column in price_df
    for date in price_dates:
        target_date = gdp_dates[gdp_counter]
        if (target_date <= date) and (gdp_counter < len(gdp_values)):
            #print(target_date, date)
            price_df.loc[price_df['Date'] == date, 'GDP'] = gdp_values[gdp_counter]
        elif (gdp_counter < (len(gdp_values) - 1)):
            gdp_counter = gdp_counter + 1

    # GDP column pre-processing
    price_df['GDP'] = price_df['GDP'].str.replace(',', '')
    price_df['GDP'] = price_df['GDP'].astype(float)
    price_df = price_df.fillna(value={'GDP':0})
    
    # Calculate price-GDP correlation
    price = price_df['Close']
    gdp = price_df['GDP']
    price_gdp_corr = price.corr(gdp)

    # load unemployment data
    unemploy_df = pd.read_csv('../../database_real/macroeconomic_data/determinants/unemployment_rate.csv', header=0)

    # load property index data
    property_df = pd.read_csv('../../database_real/macroeconomic_data/determinants/property_price.csv', header=0)

    return price_gdp_corr, 1, 1
    # return price_gdp_corr, s_unemploy, s_property


# input: @date, date to get macro data
# output: gdp, unemploy, property
def GetMacrodata(target_date):

    # get nominal GDP for target_date
    gdp_df = pd.read_csv('../../database_real/macroeconomic_data/determinants/quarterly_gdp.csv', header=0)
    gdp_dates = gdp_df['Date'].tolist()

    for date in gdp_dates:
        if (target_date < date):
            #print(target_date, date)
            gdp_series = gdp_df.loc[gdp_df['Date'] == date, 'GDP_current_market_prices']
            gdp = int(gdp_series.values[0].replace(',', ''))
            break

    # get unemployment rate for target date
    unemploy_df = pd.read_csv('../../database_real/macroeconomic_data/determinants/unemployment_rate.csv', header=0)
    ur_dates = unemploy_df['Date'].tolist()

    for date in ur_dates:
        if (target_date < date):
            #print(target_date, date)
            ur_series = unemploy_df.loc[unemploy_df['Date']
                                         == date, 'Unemployment_rate_seasonally_adjusted']
            urate = ur_series.values[0]
            break

    # get monthly property price for target date
    property_df = pd.read_csv('../../database_real/macroeconomic_data/determinants/property_price.csv', header=0)
    pp_dates = property_df['Date'].tolist()

    for date in pp_dates:
        if (target_date < date):
            #print(target_date, date)
            pp_series = property_df.loc[property_df['Date']
                                        == date, 'average_price_per_sqft']
            pprice = pp_series.values[0]
            break

    return gdp, urate, pprice


# monthly avg property price
def get_avg_property(date):
    # to type
    return True

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pandas as pd
import sys

sys.path.append("..")
mpl.use('tkagg')  # issues with Big Sur

# input: @df, stock tick df
# output: s_gdp, s_unemploy, s_property
def get_sensitivity(df):

    # load GDP data
    gdp_df = pd.read_csv('../../database_real/macroeconomic_data/determinants/TABLE030.csv',header=0)

    # load unemployment data

    # load property index data

    # return s_gdp, s_unemploy, s_property


# input: @date, date to get macro data
# output: gdp, unemploy, property
def get_macrodata(target_date):

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

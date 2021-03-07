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
    price_df['Date'] = pd.to_datetime(price_df['Date'])
    price_dates = price_df['Date'].tolist()

    """
    Correlation between stock price and quarterly nominal GDP
    """
    # load GDP data
    gdp_df = pd.read_csv('../../database_real/macroeconomic_data/determinants/quarterly_gdp.csv', header=0)
    
    gdp_df['Date'] = pd.to_datetime(gdp_df['Date'])
    gdp_dates = gdp_df['Date'].tolist()
    gdp_values = gdp_df['GDP_current_market_prices'].tolist()
    gdp_counter = 0
    #price_df['GDP'] = "0.0" # initialisation

    # merge dataframes by adding GDP column in price_df
    lower_date = gdp_dates[gdp_counter]
    upper_date = gdp_dates[gdp_counter + 1]
    
    for date in price_dates:
        if (lower_date <= date) and (date < upper_date) and (gdp_counter < len(gdp_values)):
            price_df.loc[price_df['Date'] == str(date), 'GDP'] = gdp_values[gdp_counter]

        elif (date >= upper_date) and (gdp_counter < (len(gdp_values) - 2)):
            gdp_counter = gdp_counter + 1
            price_df.loc[price_df['Date'] == date,'GDP'] = gdp_values[gdp_counter]
            lower_date = gdp_dates[gdp_counter]
            upper_date = gdp_dates[gdp_counter + 1]

    # GDP column pre-processing
    price_df['GDP'] = price_df['GDP'].str.replace(',', '')
    price_df['GDP'] = price_df['GDP'].astype(float)
    price_df = price_df.fillna(value={'GDP': 0})
    
    # Calculate price-GDP correlation
    price = price_df['Close']
    gdp = price_df['GDP']
    price_gdp_corr = price.corr(gdp)

    """
    Correlation between stock price and unemployment rate
    """
    # load unemployment data
    unemploy_df = pd.read_csv('../../database_real/macroeconomic_data/determinants/unemployment_rate.csv', header=0)

    unemploy_df['Date'] = pd.to_datetime(unemploy_df['Date'])
    ue_dates = unemploy_df['Date'].tolist()
    ue_values = unemploy_df['Unemployment_rate_seasonally_adjusted'].tolist()
    ue_counter = 0
    #price_df['Unemployment rate'] = "0.0"  # initialisation

    # merge dataframes by adding GDP column in price_df
    lower_date = ue_dates[ue_counter]
    upper_date = ue_dates[ue_counter + 1]

    for date in price_dates:
        if (lower_date <= date) and (date < upper_date) and (ue_counter < len(ue_values)):
            price_df.loc[price_df['Date'] == date, 'Unemployment rate'] = ue_values[ue_counter]

        elif (date >= upper_date) and (ue_counter < (len(ue_values) - 2)):
            ue_counter = ue_counter + 1
            price_df.loc[price_df['Date'] == date,'Unemployment rate'] = ue_values[ue_counter]
            lower_date = ue_dates[ue_counter]
            upper_date = ue_dates[ue_counter + 1]

    # unemployment column pre-processing
    price_df['Unemployment rate'] = price_df['Unemployment rate'].astype(float)
    price_df = price_df.fillna(value={'Unemployment rate': 0})

    # Calculate price-urate correlation
    price = price_df['Close']
    urate = price_df['Unemployment rate']
    price_urate_corr = price.corr(urate)
    
    """
    Correlation between stock price and monthly avg property price
    """
    # load property index data
    property_df = pd.read_csv('../../database_real/macroeconomic_data/determinants/property_price.csv', header=0)

    property_df['Date'] = pd.to_datetime(property_df['Date'])
    pp_dates = property_df['Date'].tolist()
    pp_values = property_df['average_price_per_sqft'].tolist()
    pp_counter = 0
    #price_df['Property price'] = "0.0"  # initialisation

    # merge dataframes by adding GDP column in price_df
    lower_date = pp_dates[pp_counter]
    upper_date = pp_dates[pp_counter + 1]

    for date in price_dates:
        #print(lower_date, upper_date)
        if (lower_date <= date) and (date < upper_date) and (pp_counter < len(pp_values)):
            price_df.loc[price_df['Date'] == date, 'Property price'] = pp_values[pp_counter]

        elif (date >= upper_date) and (pp_counter < (len(pp_values) - 2)):
            pp_counter = pp_counter + 1
            price_df.loc[price_df['Date'] == date, 'Property price'] = pp_values[pp_counter]
            lower_date = pp_dates[pp_counter]
            upper_date = pp_dates[pp_counter + 1]

    #print(price_df.tail())

    # pprice column pre-processing
    price_df['Property price'] = price_df['Property price'].astype(float)
    price_df = price_df.fillna(value={'Property price': 0})

    # Calculate price-urate correlation
    price = price_df['Close']
    pp = price_df['Property price']
    price_pp_corr = price.corr(pp)

    return price_gdp_corr, price_urate_corr, price_pp_corr


# input: signals dataframe
# output: signals dataframe with gdp, unemploy, property cols added
def GetMacrodata(signals):
    signals = signals.reset_index(level='Date')
    signals['Date'] = pd.to_datetime(signals['Date'])
    signals_dates = signals['Date'].tolist()

    """
    Nominal GDP (normalised)
    """
    # get nominal GDP for target_date
    gdp_df = pd.read_csv('../../database_real/macroeconomic_data/determinants/quarterly_gdp.csv', header=0)
    gdp_df['Date'] = pd.to_datetime(gdp_df['Date'])
    gdp_dates = gdp_df['Date'].tolist()
    gdp_values = gdp_df['GDP_current_market_prices'].tolist()
    gdp_counter = 0

    # merge dataframes by adding GDP column in signals
    lower_date = gdp_dates[gdp_counter]
    upper_date = gdp_dates[gdp_counter + 1]

    for date in signals_dates:
        if (lower_date <= date) and (date < upper_date) and (gdp_counter < len(gdp_values)):
            signals.loc[signals['Date'] == date,
                        'GDP'] = gdp_values[gdp_counter]
        elif (date >= upper_date) and (gdp_counter < (len(gdp_values) - 2)):
            gdp_counter = gdp_counter + 1
            signals.loc[signals['Date'] == date,
                         'GDP'] = gdp_values[gdp_counter]
            lower_date = gdp_dates[gdp_counter]
            upper_date = gdp_dates[gdp_counter + 1]
        elif (date >= upper_date) and (gdp_counter == (len(gdp_values) - 2)):
            signals.loc[signals['Date'] == date,
                        'GDP'] = gdp_values[gdp_counter]
    
    # GDP column pre-processing
    signals['GDP'] = signals['GDP'].str.replace(',', '')
    signals['GDP'] = signals['GDP'].astype(float)
    signals = signals.fillna(value={'GDP': 0})
    signals['GDP'] = (signals['GDP'] - signals['GDP'].min()) / \
        (signals['GDP'].max() - signals['GDP'].min()) # min-max normalisation

    #print(signals.tail())
    """
    Unemployment rate (normalised)
    """
    # get unemployment rate for target date
    ur_df = pd.read_csv(
        '../../database_real/macroeconomic_data/determinants/unemployment_rate.csv', header=0)
    ur_df['Date'] = pd.to_datetime(ur_df['Date'])
    ur_dates = ur_df['Date'].tolist()
    ur_values = ur_df['Unemployment_rate_seasonally_adjusted'].tolist()
    ur_counter = 0

    # merge dataframes by adding urate column in signals
    lower_date = ur_dates[ur_counter]
    upper_date = ur_dates[ur_counter + 1]

    for date in signals_dates:
        if (lower_date <= date) and (date < upper_date) and (ur_counter < len(ur_values)):
            signals.loc[signals['Date'] == date,
                        'Unemployment rate'] = ur_values[ur_counter]
        elif (date >= upper_date) and (ur_counter < (len(ur_values) - 2)):
            ur_counter = ur_counter + 1
            signals.loc[signals['Date'] == date,
                        'Unemployment rate'] = ur_values[ur_counter]
            lower_date = ur_dates[ur_counter]
            upper_date = ur_dates[ur_counter + 1]
        elif (date >= upper_date) and (ur_counter == (len(ur_values) - 2)):
            signals.loc[signals['Date'] == date,
                        'Unemployment rate'] = ur_values[ur_counter]

    # UR column pre-processing
    signals['Unemployment rate'] = signals['Unemployment rate'].astype(float)
    signals = signals.fillna(value={'Unemployment rate': 0})
    signals['Unemployment rate'] = (signals['Unemployment rate'] - signals['Unemployment rate'].min()) / \
        (signals['Unemployment rate'].max() - signals['Unemployment rate'].min())  # min-max normalisation

    #print(signals.tail())

    """
    Avg monthly property price (normalised)
    """
    # get monthly property price for target date
    pp_df = pd.read_csv(
        '../../database_real/macroeconomic_data/determinants/property_price.csv', header=0)
    pp_df['Date'] = pd.to_datetime(pp_df['Date'])
    pp_dates = pp_df['Date'].tolist()
    pp_values = pp_df['average_price_per_sqft'].tolist()
    pp_counter = 0

    # merge dataframes by adding GDP column in price_df
    lower_date = pp_dates[pp_counter]
    upper_date = pp_dates[pp_counter + 1]

    for date in signals_dates:
        if (lower_date <= date) and (date < upper_date) and (pp_counter < len(pp_values)):
            signals.loc[signals['Date'] == date,
                        'Property price'] = pp_values[pp_counter]
        elif (date >= upper_date) and (pp_counter < (len(pp_values) - 2)):
            pp_counter = pp_counter + 1
            signals.loc[signals['Date'] == date,
                        'Property price'] = pp_values[pp_counter]
            lower_date = pp_dates[pp_counter]
            upper_date = pp_dates[pp_counter + 1]
        elif (date >= upper_date) and (pp_counter == (len(pp_values) - 2)):
            signals.loc[signals['Date'] == date,
                        'Property price'] = pp_values[pp_counter]

    # PP column pre-processing
    signals['Property price'] = signals['Property price'].astype(float)
    signals = signals.fillna(value={'Property price': 0})
    signals['Property price'] = (signals['Property price'] - signals['Property price'].min()) / \
        (signals['Property price'].max() - signals['Property price'].min())  # min-max normalisation


    #print(signals.tail())
    return signals

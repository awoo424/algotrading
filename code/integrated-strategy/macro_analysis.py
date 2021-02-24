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
def get_macrodata(date):

    gdp_df = pd.read_csv('../../database_real/macroeconomic_data/determinants/TABLE030.csv', header=0)

    # to type

    # return gdp, unemploy, property

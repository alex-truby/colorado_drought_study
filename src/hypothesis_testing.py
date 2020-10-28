import pandas as pd
import numpy as np
import scipy as sp
import scipy.stats as stats
import statsmodels.api as sm

def convert_col_to_arrary(year, df, col1, col2):
    filtered_df = df[df[col1] == year]
    arr = np.array(filtered_df[col2])
    return arr

def t_p_vals(arr1, arr2):
    t, p = stats.ttest_ind(arr1, arr2, equal_var = False)
    return round(t, 3), round(p, 3)


def ols_model_fit(df, col1, col2):
    X = df[col1]
    X = sm.add_constant(X)
    Y = df[col2]
    model = sm.regression.linear_model.OLS(Y, X)
    results = model.fit()
    t_test_results = results.t_test([0,1], use_t=False)
    return t_test_results


if __name__ == '__main__':
    cleaned_data = pd.read_csv('./../capstone1/data/monthly_data_withdates.csv')
    cleaned_data['y_m'] = cleaned_data['date'].str.replace("-", "").astype(int)-20000000
    cleaned_data = cleaned_data.groupby('y_m').mean().reset_index()
    cleaned_data = cleaned_data.reset_index()
    cleaned_data.rename(columns={'index': 'month_index'}, inplace=True)

    #used for analysis of t, p values for ground water depths
    gw = cleaned_data.copy()

    #get yearly averages
    #zero nulls will skew averages - will drop any remaining nulls  in dataset
    gw.dropna(inplace=True)

    #some incorrect readings in the Water Level Depth Column - will take out anything that is <0 for analysis (typos)
    gw = gw[gw['Water Level Depth'] >0]


    #hypothesis testing comparing only data sets from 2000 v. 2016
    drought_mon_vals_2000 = convert_col_to_arrary(2000, cleaned_data, 'year', 'drought_vals')
    drought_mon_vals_2016 = convert_col_to_arrary(2016, cleaned_data, 'year', 'drought_vals')
    drought_mon_t_p = t_p_vals(drought_mon_vals_2000, drought_mon_vals_2016)
    print(f"Drought Monitor p-value for 2000 v. 2016 Comparison is: {drought_mon_t_p[1]}")

    pdsi_vals_2000 = convert_col_to_arrary(2000, cleaned_data, 'year', 'pdsi')
    pdsi_mon_vals_2016 = convert_col_to_arrary(2016, cleaned_data, 'year', 'pdsi')
    pdsi_t_p = t_p_vals(pdsi_vals_2000, pdsi_mon_vals_2016)
    print(f"Palmer Drought Severity Index p-value for 2000 v. 2016 Comparison is: {pdsi_t_p[1]}")

    spei_vals_2000 = convert_col_to_arrary(2000, cleaned_data, 'year', 'spei')
    spei_mon_vals_2016 = convert_col_to_arrary(2016, cleaned_data, 'year', 'spei')
    spei_t_p = t_p_vals(spei_vals_2000, spei_mon_vals_2016)
    print(f"Standardised Precipitation-Evapotranspiration Index p-value for 2000 v. 2016 Comparison is: {spei_t_p[1]}")

    water_depths_2000 = convert_col_to_arrary(2000, gw, 'year', 'Water Level Depth')
    water_depths_2016 = convert_col_to_arrary(2016, gw, 'year', 'Water Level Depth')
    water_depths_t_p = t_p_vals(water_depths_2000, water_depths_2016)
    print(f"Water Level Depth p-value for 2000 v. 2016 Comparison is: {water_depths_t_p[1]}")

    #linear regression confidence intervals on the slope
    print("\n", "Drought Monitor t-test Results", "\n", ols_model_fit(cleaned_data, 'month_index', 'drought_vals'))
    print("\n", "Palmer Drought Sevrity Index t-test Results", "\n", ols_model_fit(cleaned_data, 'month_index', 'pdsi'))
    print("\n", "Standardised Precipitation-Evapotranspiration Index", "\n", ols_model_fit(cleaned_data, 'month_index', 'spei'))
    print("\n", "Water Level Depth t-test Results", "\n",ols_model_fit(gw, 'month_index', 'Water Level Depth'))
    

import pandas as pd
from datetime import date

#string formatting
#removes spaces, transforms into lower case
def format_columns(df, col_name):
    df[col_name] = df[col_name].str.replace(' ', "")
    df[col_name] = df[col_name].str.lower()
    return df 

#filter df down to CO only values:
#check on this string formatting to set variable name... does this work?
def co_counties_filter(df, col_name, lst):
    new_df= df[df[col_name].isin(lst)]
    return new_df

#filter out years <2000
def filter_post_2000(df, col_name):
    df = df[df[col_name] >=2000].reset_index(drop=True)
    return df

#filter to only desired columns:
def filter_cols(df, col1, col2, col3, col4):
    df = df.loc[:, [col1, col2, col3, col4]]
    return df

#group by
def group_by_means(df, col1, col2, col3):
    df = df.groupby([col1, col2, col3]).mean().reset_index()
    return df

#join column to dataframe
def join_col(df, col_list):
    for col in col_list:
        df.join(col)
    return df 



if __name__ == '__main__':
    
    #data tablle cleaned to get County: FIPS dictinary and FIPS list to be used in joins later
    #file should be updated to reflect users file structure
    western_drought_df = pd.read_csv('./../capstone1/data/western_us_drought.csv')
    co_state_df = western_drought_df[western_drought_df['State'] == 'CO'].reset_index()
    co_state_df['County'] = co_state_df['County'].str.replace('County',"")
    
    format_columns(co_state_df, 'County')

    county_fips_dict = co_state_df.set_index('County')['FIPS'].to_dict()
    co_fips_list = [fip for fip in county_fips_dict.values()]
    #county_fips_dict will be used to as the basis of joining the data frames together 

    #US DROUGHT MONITOR DATA
    us_drought_mon_df = pd.read_csv('./../capstone1/data1/us_drought_monitor_2000-2016.csv')
    us_drought_df = us_drought_mon_df.copy()

    co_drought_df = co_counties_filter(us_drought_df, 'countyfips', co_fips_list)

    #current notation: 9 = no drought, 0 = abnormally dry, 1 = moderately dry, 2 = Severe Drought, 3 = Extreme Drought, 4 = Exceptional Drought
    #desired notation: 0 = no drought, 1 = abnormally dry, 2 = moderately dry, 3 = Severe Drought, 4 = Extreme Drought, 5 = Exceptional Drought
    new_drought_vals = {9:0, 0:1, 1:2, 2:3, 3:4, 4:5}
    co_drought_df['drought_vals'] = co_drought_df['value'].map(new_drought_vals) 

    #final co drought data by county, ready to be combined
    co_drought_df = filter_cols(co_drought_df, 'year', 'countyfips', 'drought_vals', 'month')
    co_drought_df.reset_index(drop=True)
    co_drought_df = group_by_means(co_drought_df, 'countyfips', 'year', 'month')

    #COLORADO GROUNDWATER WELL DATA FROM DEPARTMENT OF WATER RESOURCES (DWR)
    co_gw_df = pd.read_csv('./../capstone1/data1/co_dwr_well_water_level.csv', low_memory=False)
    co_wells_df = co_gw_df.copy()
    co_wells_df = format_columns(co_wells_df, 'County')

    #extract year from measurement date string for groupby later
    co_wells_df['year'] = pd.DatetimeIndex(co_wells_df['Measurement Date']).year
    co_wells_df['month'] = pd.DatetimeIndex(co_wells_df['Measurement Date']).month
    co_wells_df = filter_post_2000(co_wells_df, 'year')

    #add fips column to join on later
    co_wells_df['fips'] = co_wells_df['County'].map(county_fips_dict)

    co_wells_df = filter_cols(co_wells_df, 'Water Level Depth', 'year', 'fips', 'month')
    #sort by year
    co_wells_df.sort_values(['year'])

    #drop null values - need to drop so as to not skew average well depths
    co_wells_df.dropna(inplace=True)
    co_wells_df['fips']= co_wells_df['fips'].astype(int)

    co_wells_df = group_by_means(co_wells_df, 'fips', 'year', 'month')
    co_wells_df = co_wells_df.rename(columns = {'fips' : 'countyfips'}, inplace=False)

    #SPEI DATA
    spei_data = pd.read_csv('./../capstone1/data1/spei_1895-2016.csv') #low_memory=False)
    spei_df = spei_data.copy()

    spei_df = filter_post_2000(spei_df, 'year')
    spei_df = co_counties_filter(spei_df, 'fips', co_fips_list)
    spei_df = filter_cols(spei_df, 'year', 'fips', 'spei', 'month')
    spei_df = group_by_means(spei_df, 'fips', 'year', 'month')

    #PDSI DATA
    palmer_dsi_df = pd.read_csv('./../capstone1/data1/palmer_dsi_1895-2016.csv')
    pdsi_df = palmer_dsi_df.copy()  

    pdsi_df = filter_post_2000(pdsi_df, 'year')
    pdsi_df = co_counties_filter(pdsi_df, 'countyfips', co_fips_list)
    pdsi_df = filter_cols(pdsi_df, 'year', 'countyfips', 'pdsi', 'month')
    pdsi_df = group_by_means(pdsi_df, 'countyfips', 'year', 'month')

    #MERGE DATA
    combined_df = pdsi_df.join(spei_df['spei'])
    combined_df = combined_df.join(co_drought_df['drought_vals'])
    combined_df = group_by_means(combined_df, 'countyfips', 'year', 'month')

    final_df = combined_df.copy()
    final_df = pd.merge(final_df, co_wells_df, how='left', on=['countyfips', 'year', 'month'])
    final_df = group_by_means(final_df, 'countyfips', 'year', 'month')
    
    final_df['date'] = pd.to_datetime(final_df['year'].astype(str) + '/' + final_df['month'].astype(str))
    #only run if want another copy of the cleaned data set
    #final_df.to_csv (r'monthly_data_withdates.csv', index=False, header=True)




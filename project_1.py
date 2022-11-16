#%%
# 1
# packages for data analysis, cleaning, and plotting
import pandas as pd
import matplotlib.pyplot as plt
%matplotlib inline

# packages for text translation
import googletrans
from googletrans import Translator

#%%
# 2 and 3
# Reads a csv file and converts it into a pandas DataFrame
# Casts/parses the 'data' column's dtype from 'object' to 'datetime64[ns]'
df = pd.read_csv('amazon.csv', header=0, parse_dates=['date'], encoding='iso-8859-1')

# 3
# dataframes metadata including data types of the columns
df.info()
df.dtypes

#%%
# 4
# Top 5 rows in the dataframe
df.head()  # == df.head(5)
#%%
# 5
# Last 5 rows in the dataframe
df.tail()  # == df.tail(5)

#%%
# 6
# Shape of the dataframe ie number of rows and columns
df.count  # [row_count rows x col_count columns]
df.shape  # (row_count, col_count)
print(f'row_count: {df.shape[0]}')
print(f'col_count: {df.shape[1]}')

#%%
# 7
# Displays data type for each column
# Observation: there many different ways to check the data type of a datafram column
#              memory usage is important as the dataframe is stored in the main memory
df.dtypes['year']
df.dtypes['state']
df.dtypes['month']
df.dtypes['number']
df.dtypes['date']
df.info()

# changes 'years' column to str/object data type
df['year'] = df['year'].astype(str)

# Memory usage of each column
df.memory_usage()
df.memory_usage(index=True)  # including index column's memory usage
df.memory_usage(deep=True)   # including system level memory usage of each column of data type 'object'

#%%
# 8
# Removes duplicate elements inplace
# Observation: 'inplace' kwarg assists in saving memory
df_with_dups = len(df)
df_without_dups = 0

df.drop_duplicates(inplace=True)
df_without_dups = len(df)

#%%
# 9
# checks for NA (None, NaN, etc) values
# Observation: NA values can be searched on a axis (0 or 1)
df.isna() # == df.isnull()

df.isna().any()  # checks if there's atleast one NA (None, NaN, etc) element for each column
df['state'].isna().any()    # checks if there's atleast one NA (None, NaN, etc) element for the 'state' column
df.isna().all()  # checks if all elements are NA (None, NaN, etc) values for each column
# No NA values found

#%%
#10

#%%
#11
translator = Translator()
#translated = translator.translate('Hola Mundo')
#translated.text

#df['month'] = df['month'].apply(lambda x: translator.translate(x, dest='en').text)

#%%
# 12
# Total number of fires registered
# Answer: 698811.073
df['number'].sum()

#%%
# 13
# Returns the months with the maximum number of fires (desc) by month (asc)
# Observation: September has the max number of fires
df_13 = df.groupby('month')['number'] \
            .max().reset_index() \
            .sort_values(['number', 'month'], \
            ascending=[False, True])
plt.bar('month', 'number', data=df_13)

#%%
# 14
# Returns the years with the maximum number of fires (desc) by year (asc)
# Observation: 1. 2008, 2. 2006, 3. 2012
df_14 = df.groupby('year')['number'] \
            .max().reset_index() \
            .sort_values(['number', 'year'], \
            ascending=[False, True])
plt.bar('year', 'number', data=df_14)

#%%
# 15
# Returns the maximum number of fires (desc) by state (asc)
# Observation: 1. Amazonas, 2. Bahia, 3. Ceara
df_15 = df.groupby('state')['number'] \
            .max().reset_index() \
            .sort_values(['number', 'state'], \
            ascending=[False, True])
plt.bar('state', 'number', data=df_15.head())

#%%
# Adds 'day of week' column based on the 'date' column
df['dayofweek'] = df['date'].dt.day_name()

# 16
# Returns the total number of fires in Amazonas
# Answer: 30650.129
df_16_amazonas = df.loc[df['state'] == 'Amazonas']
df_16_amazonas['number'].sum()

#%%
# 17
# Returns the total number of fires in Amazonas (desc) by year {asc}
# Observation: 1. 2002, 2. 2008, 3. 2014
df_17_amz_fires_by_year = df_16_amazonas.groupby('year')['number'] \
                                        .sum().reset_index() \
                                        .sort_values(['number', 'year'], \
                                        ascending=[False, True])
plt.bar('year', 'number', data=df_17_amz_fires_by_year.head())

#%%
# 18
# Returns the total number of fires in Amazonas (desc) by day of week (asc)
# Observation: 1. Tuesday, 2. Thursday, 3. Friday
df_18_dow = df_16_amazonas.groupby('dayofweek')['number'] \
    .sum().reset_index() \
    .sort_values(['number', 'dayofweek'], \
    ascending=[False, True])
plt.bar('dayofweek', 'number', data=df_18_dow.head())

#%%
# 19
# Returns the total number of fires in the year 2015
# Answer: 41208.292
df_19_2015 = df.loc[df['year'] == '2015']
df_19_2015['number'].sum()

#%%
# Returns the total number of fires (desc) per month (asc) in the year 2015
# Observation: 1. January, 2. October, 3. July
df_19_2015_sum = df_19_2015 \
                .groupby('month')['number'] \
                .sum().reset_index() \
                .sort_values(['number', 'month'], \
                ascending=[False, True])
plt.bar('month', 'number', data=df_19_2015_sum.head())

#%%
# Returns the average number of fires (desc) per month (asc) in the year 2015
# Observation: 1. January, 2. October, 3. July
df_19_2015_mean = df_19_2015 \
                .groupby('month')['number'] \
                .mean().reset_index() \
                .sort_values(['number', 'month'], \
                ascending=[False, True])
plt.bar('month', 'number', data=df_19_2015_mean.head())

#%%
# 20
# Returns the average number of fires (desc) by state
# Observation: 1. Sao Paulo, 2. Mato Grosso, 3. Bahia
df_20_state = df.groupby('state')['number'] \
                .mean().reset_index() \
                .sort_values('number', ascending=False)
plt.bar('state', 'number', data=df_20_state.head())

#%%
# 21
# Returns names of the state that have had a fire in the month of December
# Answer: array(['Acre', 'Alagoas', 'Amapa', 'Amazonas', 'Bahia', 'Ceara', \
#                    'Distrito Federal', 'Espirito Santo', 'Goias', 'Maranhao', \
#                    'Mato Grosso', 'Minas Gerais', 'Parï¿½', 'Paraiba', 'Pernambuco', \
#                    'Piau', 'Rio', 'Rondonia', 'Roraima', 'Santa Catarina', \
#                    'Sao Paulo', 'Sergipe', 'Tocantins'], dtype=object)
df_21_dec = df.loc[(df['month'] == 'Dezembro') & (df['number'] > 0)]
df_21_dec['state'].unique()

#%%
# Additional

# 22
# Returns the average number of fires on average (desc) by month (asc)
# Observation: 1. July, 2. October, 3. August, 4. November, 5. December
df_22 = df.groupby('month')['number'] \
            .mean().reset_index() \
            .sort_values(['number', 'month'], \
            ascending=[False, True])
plt.bar('month', 'number', data=df_22.head())

#%%
# 23
# Returns the average number of fires (desc) by year (asc)
# Observation: 1. 2003, 2. 2016, 3. 2015, 4. 2012, 5. 2017
df_23 = df.groupby('year')['number'] \
            .mean().reset_index() \
            .sort_values(['number', 'year'], \
            ascending=[False, True])
plt.bar('year', 'number', data=df_23.head())
#%%
# 24
# Returns the average number of fires (desc) by state (asc)
# Observation: 1. Sao Paulo, 2. Mato Grosso, 3. Bahia, 4. Bahia, 5. Goias
df_24 = df.groupby('state')['number'] \
            .mean().reset_index() \
            .sort_values(['number', 'state'], \
            ascending=[False, True])
plt.bar('state', 'number', data=df_24.head())

#%%
# 25

#%%
# 26

#libraries
import pandas as pd # library to manage data frames
import numpy as np #library to manage numeric/ mathematical values
import seaborn as sns #for visualizations
import matplotlib.pyplot as plt #in connection with the library above create great visualizations
import kagglehub

# Getting Data
path = kagglehub.dataset_download("bhatvikas/world-tourism-economic-data")
df= pd.read_csv("World Indicators.csv", delimiter= ";") #had to specify the delimiter in order to have the data in different columns

# Cleaning Steps:
df.columns= [col.lower().replace(" ", "_") for col in df.columns]
df.drop(columns=["hours_to_do_tax", "ease_of_business","business_tax_rate","days_to_start_business","header","lending_interest","energy_usage","co2_emissions","internet_usage","mobile_phone_usage"], inplace= True)
data= df.copy()

# Fillnans:
data["tourism_inbound"] = round(data["tourism_inbound"].str.replace("$", "").str.replace(",", ""),2)
data["tourism_outbound"] = round(data["tourism_outbound"].str.replace("$", "").str.replace(",", ""),2)
data["tourism_inbound"]= data["tourism_inbound"].astype(float)
data["tourism_outbound"]= data["tourism_outbound"].astype(float)
data["tourism_inbound"] = data["tourism_inbound"].fillna(0)  #filling the nan with 0 to be able to calculate the mean without nan
data["tourism_outbound"] = data["tourism_outbound"].fillna(0)
mean_by_region_inbound = data.groupby('region')['tourism_inbound'].transform('mean')
data.loc[data['tourism_inbound'] == 0, 'tourism_inbound'] = mean_by_region_inbound
data["tourism_inbound"] = data["tourism_inbound"].apply(lambda x: '{:.2f}'.format(x))

#then i will do the same for tourism_outbound
mean_by_region_outbound = data.groupby('region')['tourism_outbound'].transform('mean')
data.loc[data['tourism_outbound'] == 0, 'tourism_outbound'] = mean_by_region_outbound 
data["tourism_outbound"] = data["tourism_outbound"].apply(lambda x: '{:.2f}'.format(x))

# cleaning using transform method
data["gdp"] = data["gdp"].str.replace("$", "").str.replace(",", "")
data["gdp"]= data["gdp"].astype(float)
data["gdp"] = data["gdp"].fillna(0)
mean_by_region_gdp = data.groupby('region')['gdp'].transform('mean')
data.loc[data['gdp'] == 0, 'gdp'] = mean_by_region_gdp
data["gdp"] = data["gdp"].apply(lambda x: '{:.2f}'.format(x)) 

#i got a big number that did not fit in the column so i had to format it with2 decimals

data= data.drop(columns=["health_exp_%_gdp","health_exp/capita","infant_mortality_rate","life_expectancy_female","life_expectancy_male","number_of_records","birth_rate","population_0-14","population_15-64","population_65+","population_urban"])
data["year"]=data["year"].str[-4:]

# Save our data:
data.to_csv("test_clean.csv", index=False)
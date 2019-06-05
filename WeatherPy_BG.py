#!/usr/bin/env python
# coding: utf-8

# # WeatherPy_BG
# ----
# 
# ### Analysis
# * Temperatures Peak near the equator.  However the maximum temperature is higher in the northern hempisphere, due to the tilt of the earth (summer).  However, in the northern hemisphere there were outliers which maintained a low temperature despite a moderate latitude (~40 degrees north).  This may be due to factors such as elevation.
# 
# * There are strong bands of cloudiness at 0, 40, 20 60, 80 and 100% cloudiness. This indicates a measurement error.  Because no metric exists for total cloud cover, the recording of cloud cover data forces the observed state into a category, effectively "binning" the cloud cover at the time of measurement.
# 
# * There is a spike in wind speed at -30 to -40 south latitude.  It is itneresting to consider whether latitutde has an effect. See [Trade Winds](https://en.wikipedia.org/wiki/Trade_winds) which are well documented winds occurring consistently at certain latitudes.  The increase in wind speed may be due to winter in the southern hemisphere.
# 
# ---

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import json
import time
import os
import csv

# Import API key
from api_keys import api_key

#set up target URL
url = "http://api.openweathermap.org/data/2.5/weather?"
units = "imperial"

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# ## Generate Cities List

# In[2]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


# In[3]:


#print(cities) #debug


# In[4]:


#type(lat_lngs) #debug note: this returns a zip object which acts like a tuple.


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).
# 

# In[5]:


#traverse the city list
#Include a print 
#log of each city as it'sbeing processed (with the city number and city name).

# Build query URL 
#query_url = f"{url}appid={api_key}&q={city}"#"&units={units}"
query_url = url + "appid=" + api_key + "&q=" 


# set up lists to hold reponse info
lat = []
long = []
temp = []
hum = []
cloud = []
wind = []
final_cities = []
excluded_cities =[] #probably not necessary but it doesn't hurt to keep a list of what gets tossed

#Add a progress counter
counter = 0

# Loop through the list of cities and perform a request for data on each
#NOTE: NEEDS EXCEPTION HANDLING not all cities returned by citipy may be tracked by openweather

for city in cities:
    
    #Get data    
    try:
        response = requests.get(query_url + city + "&units=" + units).json()
        lat.append(response["coord"]['lat']) #append the list of latitudes
        long.append(response['coord']['lon']) #append the list of longitudes
        temp.append(response['main']['temp_max']) #append the list of max temperatures
        hum.append(response['main']['humidity']) #append the list of hunidity values
        cloud.append(response["clouds"]["all"]) #append the list of cloud cover values
        wind.append(response["wind"]["speed"]) #append the list of wind speed
        final_cities.append(city) #build a list of the cities which returned a value and did not throw exception.
        
        #print status output
        print("Processing " + str(counter) +": Current City: " + city + "\n\t URL: " + query_url + city + "&units=" + units )
       
        counter = counter +1 #this shows progress
        
    # Catch exception if trying to access key that doesn't exist
    except KeyError: 
       #track cities which throw an exception
        excluded_cities.append(city)
        
        # print a message to notify user of city exception
        print ("Processing " + str(counter) +": Current City:" + city +"\n\t weather data not found -excluded from list") 
    
        counter = counter+1
        
    continue  #NOTE: to continue running the for loop the try/except block must be inside the for loop

print("City API calls complete") #let the user know that the call is done
    
    


# In[6]:


#debug peek at the data retrieved

#print(f"The latitude information received is: {lat}")  
#print(f"The maximum temperature information received is: {temp}")
#print(f"The longitude information received is: {long}")
#print(f"The final list of cities where data was retrieved is: {final_cities}")
#print(f"The humidity information received is: {hum}")
#print(f"The cloud information received is: {cloud}")


# In[7]:


#debug

#check the list size because equal size lists make the DataFrame constructor happy
print(len(lat))  
print(len(long))
print(len(temp))
print(len(hum))
print(len(final_cities))
print(len(excluded_cities))


# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame

# In[8]:


#NOTE:  There is a design consideration here: Can either write to a CSV and 
#read that into a DataFrame OR create a DataFrame from the available lists and use pandas
#to write to a CSV from the dataframe.  
#End result is the same, I opted to make the Dataframe first because .toCSV() method is more intuitve

#dataframe constructor

weather_df = pd.DataFrame({"City": final_cities, 
                           "Latitude": lat, 
                           "Longitude": long, 
                           "Temp": temp,
                           "Humidity": hum,
                           "Clouds": cloud,
                           "Wind": wind })
weather_df.head()


# In[9]:


weather_df.to_csv(output_data_file) #write file to CSV in the same directory


# ### Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# #### Latitude vs. Temperature Plot

# In[10]:


weather_df.plot(kind='scatter',x='Latitude',y='Temp', marker="o", edgecolors="black")
plt.title("Latitude vs. Max Temperature " + str(time.strftime("%x")))
plt.xlabel("Latitude")
plt.ylabel("Max Temperature")
plt.savefig("./LAT_TEMP_BG.png")
plt.show()


# #### Latitude vs. Humidity Plot

# In[11]:


weather_df.plot(kind='scatter',x='Latitude',y='Humidity', marker="o", edgecolors="black")
plt.title("Latitude vs. Humidity " + str(time.strftime("%x")))
plt.xlabel("Latitude")
plt.ylabel("Humidity")
plt.savefig("./LAT_HUM_BG.png")
plt.show()


# #### Latitude vs. Cloudiness Plot

# In[12]:


weather_df.plot(kind='scatter',x='Latitude', y='Clouds', marker="o", edgecolors="black")
plt.title("Latitude vs. Cloudiness " + str(time.strftime("%x")))
plt.xlabel("Latitude")
plt.ylabel("Cloudiness")
plt.savefig("./LAT_CLOUD_BG.png")
plt.show()


# #### Latitude vs. Wind Speed Plot

# In[13]:


weather_df.plot(kind='scatter',x='Latitude', y='Wind', marker="o", edgecolors="black")
plt.title("Latitude vs. Wind Speed " + str(time.strftime("%x")))
plt.xlabel("Latitude")
plt.ylabel("Wind Speed")
plt.savefig("./LAT_WIND_BG.png")
plt.show()


# In[ ]:





# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 17:12:51 2020

@author: Eirik Nordgård 

This is a short script to retrieve data from MET Norways FROST 
observations. The script retrieves the files from a givven URL using 
a client ID. Visit https://frost.met.no/api.html for detailed information on
what parameters can be obtained. Available stations can be found at 
https://seklima.met.no/observations/  
"""

# Libraries needed (pandas is not standard and must be installed in Python)
import requests
import pandas as pd

# Insert your own client ID here
client_id = 'fef2ad54-a9c5-44b8-bf88-26fd092f2a57' #my personal ID

# Define endpoint and parameters
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN12290',
    'elements': 'sum(precipitation_amount PT12H)',
    'referencetime': '2018-05-05/2020-05-05',
}
# Issue an HTTP GET request
r = requests.get(endpoint, parameters, auth=(client_id,''))
# Extract JSON data
json = r.json()

# Check if the request worked, print out any errors
if r.status_code == 200:
    data = json['data']
    print('Data retrieved from frost.met.no!')
else:
    print('Error! Returned status code %s' % r.status_code)
    print('Message: %s' % json['error']['message'])
    print('Reason: %s' % json['error']['reason'])
    
#%%
# Extract value from JSON-file (data)
temp=[]
for i in range(len(data)):
    tem = data[i]['observations'][0]['value']
    temp.append(tem)

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
fig,ax = plt.subplots()
ax.set_title('STATION SN12290, HAMAR(Disen)')
ax.set_ylabel('mm [12H]'), ax.set_xlabel('TIME')
ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
ax.plot(temp)

#%%
'''
These nex two sections creates dataframes for analysis etc.
'''
# This will return a Dataframe with all of the observations in a table format
df = pd.DataFrame()
for i in range(len(data)):
    row = pd.DataFrame(data[i]['observations'])
    row['referenceTime'] = data[i]['referenceTime']
    row['sourceId'] = data[i]['sourceId']
    df = df.append(row)

df = df.reset_index()

df.head()
#%%
# This returns a simpler Dataframe than the one above
# These additional columns will be kept
columns = ['sourceId','referenceTime','elementId','value','unit','timeOffset']
df2 = df[columns].copy()
# Convert the time value to something Python understands
df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])
# Preview the result
df2.head()
#%%
' A possbile tick fix: https://stackoverflow.com/questions/46218972/x-axis-label-at-start-end-of-chart-in-matplotlib'

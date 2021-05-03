#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 10:32:39 2020

@author: joshuak
"""

# https://dev.fitbit.com/build/reference/web-api/oauth2/#implicit-grant-flow

# Selenium Documentation:
# https://selenium-python.readthedocs.io/locating-elements.html

#Import the necessary packages
from time import sleep
import fitbit
import pandas as pd
import datetime
import json
import csv
import sys
import requests

# import other codes
#import BiometricPrevious 
import BiometricPrevious_getDevice_v2 as BiometricPrevious
import gather_keys_oauth2_copy as Oauth2

class FitbitBot:
    def __init__(self, EMAIL, PASSWORD, DATE):

        #Both the Client ID and Client Secret come from when Fitbit site after registering an app
        CLIENT_ID = '22BH28' #Mine:'22BKP3'
        CLIENT_SECRET = '78a4838804c1ff0983591e69196b1c46' #Mine:'1a42e97b6b4cc640572ae5cf10a7d0b0'
        #Authorization Process
        # opens website
        server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
        # opens website 
        server.browser_authorize(EMAIL, PASSWORD)

        ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
        REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
        auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, Oauth2=True, access_token=ACCESS_TOKEN,
        refresh_token=REFRESH_TOKEN)
        BiometricPrev = BiometricPrevious.FitbitModel1(auth2_client)
        
        biometricDF = BiometricPrev.getBiometricData(DATE) #append to data frame
        title = './CSV_Files/user' + str(i) + '_' + DATE + '.csv'
        biometricDF.to_csv(title)
        
        '''
        data = pd.read_csv(title)
        url = "http://localhost:3000/user"
        for index, row in data.iterrows():
            obj = {'collection_date': row["Date"],
                'steps': row["Steps"],
                'floors_climbed': row["Floors Climbed"],
                'total_miles': row["Total Miles"],
                'lightly_active_miles': ["Lightly Active Miles"],
                'moderately_active_miles': row["Moderately Active Miles"],
                'very_active_miles': row["Very Active Miles"],
                'sedentary_minutes': row["Sedentary Minutes"],
                'lightly_active_minutes': row["Lightly Active Minutes"],
                'fairly_active_minutes': row["Fairly Active Minutes"],
                'very_active_minutes': row["Very Active Minutes"],
                'hr30_100_minutes': row["HR 30-100 Minutes"],
                'hr100_140_minutes': row["HR 100-140 Minutes"],
                'hr140_170_minutes': row["HR 140-170 Minutes"],
                'hr170_220_minutes': row["HR 170-220 Minutes"],
                'average_resting_heartrate': row["Average Resting HR"],
                'bmi': row["BMI"],
                'sleep_efficiency': row["Sleep Efficiency"],
                'weight': row["Weight"],
                # "minutes_asleep": row["Minutes Alseep"],
                'fbusername': row["username"]
                }

            x = requests.post(url, data=obj)
        print("Database Appended")
        '''
        print("Python Script Executed")

# Initialize Emails and Passwords lists
Emails = []
Passwords = []

# Create Emails and Passwords lists from Fitbit_Credentials.csv
with open("Fitbit_Credentials.csv") as File1:
    IDs = csv.DictReader(File1)
    for row in IDs:
        Emails.append(row['Username'])
        Passwords.append(row['Password'])

# Run data extraction
for i in range(len(Emails)):
    today = str((datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d"))
    FitbitBot(Emails[i], Passwords[i], today)

# Append to database
#file = str(sys.argv[1])
#data = pd.read_csv(file)



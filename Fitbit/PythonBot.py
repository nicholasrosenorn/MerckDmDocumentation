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
 
# using sqlalchemy
import sqlalchemy as sal
from sqlalchemy import create_engine
import pandas as pd

# import other codes
import BiometricPrevious_getDevice_v2 as BiometricPrevious
import gather_keys_oauth2 as Oauth2
 

def appendDataBase(DATA,ENGINE, USER, ID):
    obj = pd.DataFrame()
   
    obj['patient_id'] = [ID]
    obj['fbusername'] = [USER]
    obj['collection_date'] = [DATA.get("Date")]
    obj['steps'] = [DATA.get("Steps")]
    obj['floors_climbed'] = [DATA.get("Floors Climbed")]
    obj['total_miles'] = [DATA.get("Total Miles")]
    obj['lightly_active_miles'] = [DATA.get("Lightly Active Miles")]
    obj['moderately_active_miles'] = [DATA.get("Moderately Active Miles")]
    obj['very_active_miles'] = [DATA.get("Very Active Miles")]
    obj['sedentary_minutes'] = [DATA.get("Sedentary Minutes")]
    obj['lightly_active_minutes'] = [DATA.get("Lightly Active Minutes")]
    obj['fairly_active_minutes'] = [DATA.get("Fairly Active Minutes")]
    obj['very_active_minutes'] = [DATA.get("Very Active Minutes")]
    obj['hr30_100_minutes'] = [DATA.get("HR 30-100 Minutes")]
    obj['hr100_140_minutes'] = [DATA.get("HR 100-140 Minutes")]
    obj['hr140_170_minutes'] = [DATA.get("HR 140-170 Minutes")]
    obj['hr170_220_minutes'] = [DATA.get("HR 170-220 Minutes")]
    obj['average_resting_hr'] = [DATA.get("Average Resting HR")]
    obj['bmi'] = DATA.get("BMI")
    obj['sleep_efficiency'] = DATA.get("Sleep Efficiency")
    obj['weight'] = DATA.get("Weight")
    # obj["minutes_asleep"] = todaysData.get("Minutes Alseep")
 
    obj.to_sql("fitbit_data", con=ENGINE, if_exists='append', index= False)
   
    return(None)
 
class FitbitBot:
    def __init__(self, EMAIL, PASSWORD, DATE, usernames, ID):
 
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
        bioDict, biometricDF = BiometricPrev.getBiometricData(DATE) #append to data frame
        title = './CSV_Files/user' + str(i) + '_' + DATE + '.csv'

        appendDataBase(bioDict,engine,usernames,ID)
        print("Python Script Executed")


# establish connecttion URL
conn = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
    'cb3i17t0aqn6a4ff', 'e2l4k9zn24shcj42', 'rnr56s6e2uk326pj.cbetxkdyhwsb.us-east-1.rds.amazonaws.com', '3306', 'lfry112yqr3k2dfr')
 
# create engine
engine = sal.create_engine(conn)
 
# Initialize user arrays
df1 = pd.read_sql_query("SELECT * FROM patient", engine)
emails = []
passwords = []
IDs = []
usernames = []
for i in range(len(df1)):
    emails.append(df1.email[i])
    passwords.append(df1.fitbit_password[i])
    IDs.append(df1.patient_id[i])
    usernames.append(df1.username[i])

today = str((datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d"))
# Run data extraction
for i in range(len(emails)):
    FitbitBot(emails[i], passwords[i], today, usernames[i], IDs[i])



'''
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

#class FitbitBot:
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
        print("Python Script Executed")

# Initialize Emails and Passwords lists
Emails = []
Passwords = []
import os

"""
Created on Wed Sep 16 10:32:39 2020
 
@author: joshuak
"""
 
# https://dev.fitbit.com/build/reference/web-api/oauth2/#implicit-grant-flow
 
# Selenium Documentation:
# https://selenium-python.readthedocs.io/locating-elements.html
 




 

'''